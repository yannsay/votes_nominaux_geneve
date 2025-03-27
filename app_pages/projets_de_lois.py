import streamlit as st
import datetime

from src.services import *
st.set_page_config(layout="wide",
                   page_title="Vote nominaux par projets de loi")

from src.repository import AppDatabase

app_database = AppDatabase()

st.title('Vote nominaux du Grand Conseil de Genève')

# Side bar filters
st.sidebar.header("Filtrez par:")
st.sidebar.subheader("- Votes")
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

st.sidebar.subheader("- Député.e.s")
selector_persons: list[str] = st.sidebar.multiselect("Selectionnez le nom",
                                                options=app_database.clean_persons_persons)
selector_parties: list[str] = st.sidebar.multiselect("Selectionnez les partis",
                                                    options=app_database.clean_persons_parties)
selector_genre: list[str] = st.sidebar.multiselect("Selectionnez le genre",
                                                    options=app_database.clean_persons_genres)

# App logic
## Filter the voting table
voting_table = filter_voting(voting_table=app_database.clean_voting,
                             selected_rubriques=selector_rubriques,
                             selected_chapitre=selector_chapitre,
                             selected_dates=selector_dates)

## Filter the votes
votes_table = filter_votes(votes_table=app_database.clean_votes,
                           persons_table=app_database.clean_persons,
                           selected_persons = selector_persons,
                           selected_parties=selector_parties,
                           selected_genre=selector_genre)

## Create the final table
table_to_plot = create_table_to_plot(
    voting_table=voting_table, votes_table=votes_table)

## Plot the final table
with st.container(height=600, key="table_votes"):
    st.write(plot_votes(table_to_plot), unsafe_allow_html=True)

st.write("Information en plus")
## Create the extra information table
voting_table_to_plot = create_info_table(voting_table = app_database.clean_voting, data_to_plot = table_to_plot)

## Plot the extra information table
with st.container(height=600, key="table_votings"):
    #voting_table_to_plot = create_info_table(table_to_plot)
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
