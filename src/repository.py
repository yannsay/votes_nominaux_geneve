import streamlit as st
import pandas as pd
import datetime

VOTING_CSV = ('inputs/voting_body.csv')
VOTES_CSV = ('inputs/votes.csv')
RSGE_CSV = ("inputs/rsGE.csv")
PERSON_CSV = ('inputs/persons.csv')

@st.cache_data
def load_data(csv_path):
    if csv_path == "inputs/rsGE.csv":
        data = pd.read_csv(csv_path, sep = ";")
    else:
        data = pd.read_csv(csv_path)
    return data

class AppDatabase:
    def __init__(self) -> None:
        self.set_clean_rsge(RSGE_CSV)
        self.set_clean_voting(VOTING_CSV, rsge_data = self.clean_rsge)
        self.set_clean_votes(VOTES_CSV, voting_data = self.clean_voting)
        self.set_clean_persons(PERSON_CSV, votes_data = self.clean_votes)

        self.set_rubriques_rsge(clean_rsge = self.clean_rsge)
        self.set_clean_persons_x(clean_persons = self.clean_persons)
        self.set_min_max_dates(clean_votings = self.clean_voting)

    def set_clean_voting(self, votings_file: str, rsge_data: pd.DataFrame) -> None:
        """
        Setter for the voting table
        Clean the voting table and add the information from RSGE
        """
        clean_voting = load_data(votings_file)
        
        # Extract Référence from title.  \xa0 is a type of white space
        pattern = r'([A-Z] [0-9] [0-9]{2}|[A-Z]\xa0[0-9]\xa0[0-9]{2})'
        clean_voting['Référence'] = clean_voting['voting_affair_title_fr'].str.extract(pattern) 
        clean_voting['Référence'] = clean_voting['Référence'].str.replace('\xa0', ' ', regex=False)

        # Add the type of vote       
        pattern = r'([A-Z]{1,2})'
        clean_voting['type_vote'] = clean_voting['voting_affair_number'].str.extract(pattern)
        
        # Filter out text without a Référence from RSGE
        clean_voting = clean_voting.loc[~pd.isna(clean_voting['Référence']),].reset_index()

        # Remove columns that are empty or not used
        column_missing :str = []
        for column in clean_voting.columns:
            if all(pd.isna(clean_voting[column])):
                column_missing.append(column)
        clean_voting = clean_voting.drop(columns = column_missing + ["index", "voting_body_key", "voting_updated_local", "voting_created_local"])

        # Add RSGE information to voting
        clean_rsge = rsge_data
        clean_voting= clean_voting.merge(clean_rsge, on = "Référence", how = "left")
        
        # Clean dates for filter in streamlit
        clean_voting["voting_date"] = pd.to_datetime(clean_voting["voting_date"])  

        self.clean_voting = clean_voting

    
    def set_clean_votes(self, votes_file: str, voting_data: pd.DataFrame) -> None:
        """
        Setter the votes table
        """
        votes_raw= load_data(votes_file)

        # Translates votes
        vote_dict = pd.DataFrame({"vote_vote":["yes", "no", "abstention"],
                                  "vote_label":["Oui", "Non", "Abstention"]})
        clean_votes = votes_raw.merge(vote_dict, how = "left",on = "vote_vote")

        clean_votes = clean_votes.drop(columns = ["vote_body_key", "vote_created_local", "vote_vote_display_de", "vote_vote_display_it", "vote_vote"]) 
        clean_votes = clean_votes[clean_votes["vote_voting_external_id"].isin(voting_data["voting_external_id"])]

        self.clean_votes = clean_votes
        
    def set_clean_persons(self, persons_file: str, votes_data) -> None:
        """
        Setter for clean persons data
        """
        persons_raw= load_data(persons_file)

        columns_to_keep = ["person_external_id", "person_fullname", "person_firstname", "person_lastname",
                            "person_party_fr", "person_website_parliament_url_fr", "person_image_url", 
                            "person_birthday", "person_occupation_fr", "person_gender", 
                            "person_function_latest_fr"]
        clean_persons = persons_raw[columns_to_keep]

        # Filter the persons that votes are in the period
        clean_persons = clean_persons[clean_persons["person_external_id"].isin(votes_data["vote_person_external_id"])]
        
        self.clean_persons = clean_persons

        
    def set_clean_rsge(self, rsge_file: str) -> None:
        """
        Setter for RSGE.
        Import the Rubriques Systématique Genève rubriques and chapters and clean them.
        """
        rsge = load_data(rsge_file)
        rubriques_mask = rsge["Référence"].str.len() == 1
        rubriques_rsge = rsge.loc[rubriques_mask]
        rubriques_rsge = rubriques_rsge.reset_index().drop(columns=["index","Date d’adoption"])
        rubriques_rsge.columns = ["Rubrique", "Intitulé rubrique"]

        chapitres_mask = (rsge["Référence"].str.len() > 1) & (rsge["Référence"].str.len() <=4)
        chapitres_rsge = rsge.loc[chapitres_mask]
        chapitres_rsge = chapitres_rsge.reset_index().drop(columns=["index","Date d’adoption"])
        chapitres_rsge.columns = ["Chapitre", "Intitulé chapitre"]

        reformatted_rsge = rsge.loc[~(chapitres_mask | rubriques_mask)]
        reformatted_rsge = reformatted_rsge.loc[~pd.isna(reformatted_rsge["Référence"])]
        reformatted_rsge = reformatted_rsge.reset_index().drop(columns=["index","Date d’adoption"])
        reformatted_rsge["Rubrique"] = reformatted_rsge['Référence'].str[0]
        reformatted_rsge["Chapitre"] = reformatted_rsge['Référence'].str[:3]
        reformatted_rsge = reformatted_rsge.merge(chapitres_rsge, on= "Chapitre", how="left").merge(rubriques_rsge, on = "Rubrique", how = "left")
        self.clean_rsge = reformatted_rsge

    def set_rubriques_rsge(self, clean_rsge: pd.DataFrame) -> None:
        """
        Create list for selector in streamlit.
        """
        rubriques_rsge = clean_rsge[["Rubrique", "Intitulé rubrique"]].drop_duplicates(
            ["Rubrique", "Intitulé rubrique"]).sort_values(by=["Rubrique"])
        self.rubriques_rsge = rubriques_rsge["Intitulé rubrique"].to_list()

    def set_clean_persons_x(self, clean_persons: pd.DataFrame) -> None:
        self.clean_persons_parties = clean_persons.drop_duplicates(
            ["person_party_fr"])["person_party_fr"].sort_values().to_list()
        self.clean_persons_genres = clean_persons.drop_duplicates(
            ["person_gender"])["person_gender"].sort_values().to_list()
        self.clean_persons_persons = clean_persons.drop_duplicates(
            ["person_fullname"])["person_fullname"].sort_values().to_list()        
    def set_min_max_dates(self, clean_votings: pd.DataFrame) -> None:
        self.min_date = clean_votings["voting_date"].min()
        self.max_date = clean_votings["voting_date"].max() + datetime.timedelta(days=1)


if __name__ == '__main__':
    # Write csv for tests
    app_database = AppDatabase()
    app_database.clean_votings.to_csv("pl_voting_clean.csv", index = False)
    app_database.clean_votes.to_csv("clean_votes.csv", index = False)
    app_database.clean_persons.to_csv("clean_persons.csv", index = False)