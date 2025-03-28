import streamlit as st
import pandas as pd
import datetime

VOTING_CSV = ('outputs/pl_voting_clean.csv')
VOTES_CSV = ('outputs/clean_votes.csv')
RSGE_CSV = ("inputs/rsGE.csv")
PERSON_CSV = ('outputs/clean_persons.csv')

@st.cache_data
def load_data(csv_path):
    if csv_path == "inputs/rsGE.csv":
        data = pd.read_csv(csv_path, sep = ";")
    else:
        data = pd.read_csv(csv_path)
    return data

class AppDatabase:
    def __init__(self) -> None:
        self.set_clean_voting(VOTING_CSV)
        self.set_clean_votes(VOTES_CSV)
        self.set_rubriques_rsge(RSGE_CSV)
        self.set_clean_persons(PERSON_CSV)
        self.set_clean_persons_x(clean_persons = self.clean_persons)
        self.set_min_max_dates(clean_votings = self.clean_voting)

    def set_clean_voting(self, votings_file: str) -> None:
        self.clean_voting = load_data(votings_file)
        self.clean_voting["voting_date"] = pd.to_datetime(self.clean_voting["voting_date"])  
    
    def set_clean_votes(self, votes_file: str) -> None:
        self.clean_votes = load_data(votes_file)
        
    def set_clean_persons(self, persons_file: str) -> None:
        self.clean_persons = load_data(persons_file)
        self.clean_persons = self.clean_persons[self.clean_persons["person_external_id"].isin(
            self.clean_votes["vote_person_external_id"])]
        
    def set_rubriques_rsge(self, rsge_file: str) -> None:
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

        final_rubriques_rsge = reformatted_rsge[["Rubrique", "Intitulé rubrique"]].drop_duplicates(
            ["Rubrique", "Intitulé rubrique"]).sort_values(by=["Rubrique"])
        self.rubriques_rsge = final_rubriques_rsge["Intitulé rubrique"].to_list()

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


