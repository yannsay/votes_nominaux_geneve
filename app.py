import streamlit as st
import datetime

from src.services import *
st.set_page_config(layout="wide")

from src.repository import AppDatabase

app_database = AppDatabase()

st.title('Vote nominaux du Grand Conseil de Genève')

st.sidebar.header("Filtrez")
st.sidebar.subheader("Votes")
selector_rubriques: list[str] = st.sidebar.multiselect("Selectionnez les rubriques",
                                                       options=app_database.rubriques_rsge)

chapitre_names = app_database.clean_voting.loc[app_database.clean_voting["Intitulé rubrique"].isin(
    selector_rubriques)]["Intitulé chapitre"].unique()

selector_chapitre: list[str] = st.sidebar.multiselect("Selectionnez les chapitres",
                                                      options=chapitre_names)

selector_dates: tuple[datetime.date] = st.sidebar.date_input("Select dates",
                                                             [app_database.min_date, app_database.max_date],
                                                             min_value=app_database.min_date,
                                                             max_value=app_database.max_date)

st.sidebar.subheader("Député.e.s")

selector_parties: list[str] = st.sidebar.multiselect("Selectionnez les partis",
                                                     options=app_database.clean_persons_parties)
selector_genre: list[str] = st.sidebar.multiselect("Selectionnez le genre",
                                                   options=app_database.clean_persons_genres)

voting_table = filter_voting(voting_table=app_database.clean_voting,
                             selected_rubriques=selector_rubriques,
                             selected_chapitre=selector_chapitre,
                             selected_dates=selector_dates)

votes_table = filter_votes(votes_table=app_database.clean_votes,
                           persons_table=app_database.clean_persons,
                           selected_parties=selector_parties,
                           selected_genre=selector_genre)

table_to_plot = create_table_to_plot(
    voting_table=voting_table, votes_table=votes_table)

with st.container(height=600, key="table_votes"):
    st.write(plot_votes(table_to_plot), unsafe_allow_html=True)

with st.container(height=600, key="table_votings"):
    #voting_table_to_plot = create_info_table(table_to_plot)
    voting_table_to_plot = create_info_table(voting_table = app_database.clean_voting, data_to_plot = table_to_plot)
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
