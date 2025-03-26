import streamlit as st
import pandas as pd
import datetime
from great_tables import GT

from src.services import *

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
rubriques_rsge = rsge[["Rubrique", "Intitulé rubrique"]].drop_duplicates(
    ["Rubrique", "Intitulé rubrique"]).sort_values(by=["Rubrique"])

clean_persons = load_data(PERSON_CSV)
clean_persons = clean_persons[clean_persons["person_external_id"].isin(
    clean_votes["vote_person_external_id"])]
clean_persons_parties = clean_persons.drop_duplicates(
    ["person_party_fr"])["person_party_fr"].sort_values()
# clean_persons_metiers = clean_persons.drop_duplicates(["person_occupation_fr"])["person_occupation_fr"].sort_values()
clean_persons_genres = clean_persons.drop_duplicates(
    ["person_gender"])["person_gender"].sort_values()

st.sidebar.header("Filtrez")
st.sidebar.subheader("Votes")

selector_rubriques: list[str] = st.sidebar.multiselect("Selectionnez les rubriques",
                                                       options=rubriques_rsge["Intitulé rubrique"])

chapitre_names = pl_voting_clean.loc[pl_voting_clean["Intitulé rubrique"].isin(
    selector_rubriques)]["Intitulé chapitre"].unique()
selector_chapitre: list[str] = st.sidebar.multiselect("Selectionnez les chapitres",
                                                      options=chapitre_names)

min_date = pl_voting_clean["voting_date"].min()
max_date = pl_voting_clean["voting_date"].max() + datetime.timedelta(days=1)

selector_dates: tuple[datetime.date] = st.sidebar.date_input("Select dates",
                                                             [min_date, max_date],
                                                             min_value=min_date,
                                                             max_value=max_date)

st.sidebar.subheader("Député.e.s")

selector_parties: list[str] = st.sidebar.multiselect("Selectionnez les partis",
                                                     options=clean_persons_parties)
selector_genre: list[str] = st.sidebar.multiselect("Selectionnez le genre",
                                                   options=clean_persons_genres)

voting_table = filter_voting(voting_table=pl_voting_clean,
                             selected_rubriques=selector_rubriques,
                             selected_chapitre=selector_chapitre,
                             selected_dates=selector_dates)

votes_table = filter_votes(votes_table=clean_votes,
                           persons_table=clean_persons,
                           selected_parties=selector_parties,
                           selected_genre=selector_genre)

table_to_plot = create_table_to_plot(
    voting_table=voting_table, votes_table=votes_table)

with st.container(height=600, key="table_votes"):
    st.write(plot_votes(table_to_plot), unsafe_allow_html=True)

with st.container(height=600, key="table_votings"):
    #voting_table_to_plot = create_info_table(table_to_plot)
    voting_table_to_plot = create_info_table(voting_table = pl_voting_clean, data_to_plot = table_to_plot)
    st.write(plot_voting(voting_table_to_plot,
             "Lien Grand Conseil"), unsafe_allow_html=True)


# csv = table_to_plot.to_csv(index=False).encode('utf-8')

# st.download_button(
#     "Cliquez pour télécharger",
#     csv,
#     f"votes_{datetime.datetime.today().strftime('%Y-%m-%d%H:%M:%S')}.csv",
#     mime="text/csv",
#     key='download-csv'
# )
