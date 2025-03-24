import streamlit as st
import pandas as pd
from datetime import datetime
from great_tables import GT, html
st.set_page_config(layout="wide")

st.title('Vote nominaux du Grand Conseil de Genève')

VOTING_CSV = ('outputs/pl_voting_clean.csv')
VOTES_CSV = ('outputs/clean_votes.csv')
RSGE_CSV = ("outputs/reformatted_rsge.csv")
PERSON_CSV = ('outputs/clean_persons.csv')

@st.cache_data
def load_data(csv_path):
    data = pd.read_csv(csv_path)
    return data

pl_voting_clean = load_data(VOTING_CSV)
pl_voting_clean["voting_date"] = pd.to_datetime(pl_voting_clean["voting_date"])

clean_votes = load_data(VOTES_CSV)
rsge = load_data(RSGE_CSV)
rubriques_rsge = rsge[["Rubrique", "Intitulé rubrique"]].drop_duplicates(["Rubrique", "Intitulé rubrique"]).sort_values(by=["Rubrique"])

clean_persons = load_data(PERSON_CSV)
clean_persons = clean_persons[clean_persons["person_external_id"].isin(clean_votes["vote_person_external_id"])]
clean_persons_parties = clean_persons.drop_duplicates(["person_party_fr"])["person_party_fr"].sort_values()
clean_persons_metiers = clean_persons.drop_duplicates(["person_occupation_fr"])["person_occupation_fr"].sort_values()
clean_persons_genres = clean_persons.drop_duplicates(["person_gender"])["person_gender"].sort_values()


def prepare_data() -> pd.DataFrame:
    min_date = pl_voting_clean["voting_date"].min()
    max_date = pl_voting_clean["voting_date"].max()
    
    st.sidebar.header("Filters")
    st.sidebar.subheader("Votes")

    selected_dates: tuple[datetime.date] = st.sidebar.date_input("Select dates", [min_date, max_date], min_value=min_date, max_value=max_date)
    selected_dates: tuple[datetime.datetime] = (pd.to_datetime(selected_dates[0]), pd.to_datetime(selected_dates[1]))


    selected_rubriques: list[str] = st.sidebar.multiselect("Selectionnez les rubriques", 
                                                           options=rubriques_rsge["Intitulé rubrique"])

    chapitre_names = pl_voting_clean.loc[pl_voting_clean["Intitulé rubrique"].isin(selected_rubriques)]["Intitulé chapitre"].unique()
    selected_chapitre: list[str] = st.sidebar.multiselect("Selectionnez les chapitres", 
                                                         options=chapitre_names)
    
    st.sidebar.subheader("Député.e.s")
    selected_parties: list[str] = st.sidebar.multiselect("Selectionnez les partis", 
                                                           options=clean_persons_parties)
    selected_metiers: list[str] = st.sidebar.multiselect("Selectionnez les métiers", 
                                                           options=clean_persons_metiers)    
    selected_genre: list[str] = st.sidebar.multiselect("Selectionnez le genre", 
                                                           options=clean_persons_genres)
    filtered_df = pl_voting_clean.copy()
    try:
        filtered_df = filtered_df[filtered_df["voting_date"].between(selected_dates[0], selected_dates[1])]

    except:
        st.error("Please select start date and end date")
        return

    if selected_rubriques != []:
        filtered_df = filtered_df[filtered_df["Intitulé rubrique"].isin(selected_rubriques)]
    if selected_chapitre != []:
        filtered_df = filtered_df[filtered_df["Intitulé chapitre"].isin(selected_chapitre)]

    title_what = "voting_title_fr" #"voting_external_id" #  
    full_table = filtered_df.merge(clean_votes, left_on = "voting_external_id", right_on="vote_voting_external_id")
    short_test = full_table.sort_values(by = "voting_date").loc[:,[title_what, "vote_person_fullname", "vote_label"]]
    table_to_plot = short_test.pivot(columns = title_what, index = "vote_person_fullname", values = "vote_label")
    table_to_plot = table_to_plot.reset_index()  
    table_to_plot = table_to_plot.rename(columns={'vote_person_fullname': 'Député.e'})

    return table_to_plot

def plot_votes(data_to_plot: pd.DataFrame) -> str:
    votes_columns = data_to_plot.columns[1:].to_list()
    return (
        GT(data_to_plot)
        .data_color(
            columns=votes_columns,
            palette=["#004D40","#D81B60", "#FFC107"],
            domain = ["Oui","Non", "Abstention"],
            na_color = "white"
            )
    )

def create_info_table(data_to_plot: pd.DataFrame) -> pd.DataFrame:
    filtered_voting = pl_voting_clean[pl_voting_clean["voting_title_fr"].isin(data_to_plot.columns)]
    filtered_voting["lien_grand_conseil"] = "https://ge.ch/grandconseil/m/search?search=" + filtered_voting["voting_title_fr"]
    filtered_voting["lien_grand_conseil"] = filtered_voting["lien_grand_conseil"].str.replace(" ", "%20")
    columns_to_keep = ["voting_affair_number", "voting_date","voting_title_fr","voting_affair_title_fr", "lien_grand_conseil", "voting_results_yes", "voting_results_no", "voting_results_abstention","type_vote", "Référence", "Intitulé rubrique", "Intitulé chapitre", "Intitulé"]
    clean_voting = filtered_voting.loc[:,columns_to_keep]

    dictionnaire_name = {"voting_affair_number":"Identifiant affaire", 
                         "voting_date": "Date du vote",
                         "voting_title_fr": "Titre du vote",
                         "voting_affair_title_fr": "Titre affaire", 
                         "lien_grand_conseil": "Lien Grand Conseil", 
                         "voting_results_yes": "Résultat - Oui", 
                         "voting_results_no": "Résutlat - Non", 
                         "voting_results_abstention": "Résultat - Abstention",
                         "type_vote" : "Type de vote", }
    clean_voting = clean_voting.rename(columns = dictionnaire_name)
    clean_voting = clean_voting.reset_index()
    clean_voting = clean_voting.drop(columns="index")

    return clean_voting

def plot_voting(data_to_plot: pd.DataFrame, links_column: str) -> str:
    data_to_plot[links_column] = "[" + data_to_plot[links_column] + "](" + data_to_plot[links_column] + ")"
    # votes_columns = data_to_plot.columns[1:].to_list()
    return (
        GT(data_to_plot)
        .fmt_markdown(columns=links_column)
        .cols_width(
        cases={
            links_column: "10%"
        })
    )

table_to_plot = prepare_data()
st.write(table_to_plot.shape)

@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

csv = convert_df(table_to_plot)

st.download_button(
   "Cliquez pour télécharger",
   csv,
   f"votes_{datetime.today().strftime('%Y-%m-%d%H:%M:%S')}.csv",
   mime="text/csv",
   key='download-csv'
)

with st.container(height=600, key="table_votes"):
    st.write(plot_votes(table_to_plot).as_raw_html(), unsafe_allow_html=True)


with st.container(height=600, key="table_votings"):
    voting_table_to_plot = create_info_table(table_to_plot)
    # st.write(voting_table_to_plot)
    st.write(plot_voting(voting_table_to_plot, "Lien Grand Conseil").as_raw_html(), unsafe_allow_html=True)
