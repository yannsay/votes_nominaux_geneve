import streamlit as st
import datetime

from src.services import *
st.set_page_config(layout="wide",
                   page_title="Votes nominaux",
                   page_icon =":envelope_with_arrow:")

from src.repository import AppDatabase

app_database = AppDatabase()

st.title('Votes nominaux du Grand Conseil de Genève - Non RSge')

# Side bar filters
st.sidebar.header("Filtrez par:")
st.sidebar.subheader("- Votes")
selector_type_votes: list[str] = st.sidebar.multiselect("Selectionnez type de votes", 
                                                        default = "Initiative populaire cantonale",
                                                        options = app_database.type_votes)
selector_dates: tuple[datetime.date] = st.sidebar.date_input("Selectionnez les dates",
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
types_votes_no_brackets = ", ".join(selector_type_votes)
st.markdown(f"**Filtre actif: {types_votes_no_brackets}**")

if selector_type_votes == []:
    titre_names = app_database.clean_oth_voting["voting_affair_title_fr"].unique()
else:
    titre_names = app_database.clean_oth_voting.loc[app_database.clean_oth_voting["type_vote_label"].isin(
        selector_type_votes)]["voting_affair_title_fr"].unique()
selector_titre: list[str] = st.multiselect("Recherche par titre",
                                        options=titre_names)

## Filter the voting table
voting_table = filter_oth_voting(voting_table=app_database.clean_oth_voting,
                              selected_type_votes=selector_type_votes,
                             selected_titres=selector_titre,
                             selected_dates=selector_dates)
## Filter the votes
votes_table = filter_votes(votes_table=app_database.clean_votes,
                           persons_table=app_database.clean_persons,
                           selected_persons = selector_persons,
                           selected_parties=selector_parties,
                           selected_genre=selector_genre)
## Create the final table
table_to_plot = create_table_to_plot( voting_table=voting_table, votes_table=votes_table)
## Plot the final table
votes_columns = table_to_plot.columns[1:].to_list()

st.dataframe(table_to_plot.style.map(color_picker,palette = palette_votes, subset=votes_columns), 
             hide_index=True)

st.write("Information en plus")
## Create the extra information table
info_table_to_plot = create_info_table(voting_table = app_database.clean_oth_voting, 
                                         data_to_plot = table_to_plot,
                                         rgse_type = False)
## Plot the extra information table
st.dataframe(info_table_to_plot, 
             column_config={"Lien Grand Conseil": st.column_config.LinkColumn("Lien Grand Conseil")}, 
             hide_index=True)
