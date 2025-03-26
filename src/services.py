"""Functions for the application"""
import datetime
import pandas as pd
import streamlit as st


def filter_voting(voting_table: pd.DataFrame,
                  selected_rubriques: list[str],
                  selected_chapitre: list[str],
                  selected_dates: tuple[datetime.date]) -> pd.DataFrame:
    """
    Function to filter the voting table
    """

    selected_dates: tuple[datetime.datetime] = (pd.to_datetime(
        selected_dates[0]), pd.to_datetime(selected_dates[1]))

    filtered_df = voting_table.copy()
    try:
        filtered_df = filtered_df[filtered_df["voting_date"].between(
            selected_dates[0], selected_dates[1], inclusive="both")]

    except:
        st.error("Please select start date and end date")
        return

    if selected_rubriques != []:
        filtered_df = filtered_df[filtered_df["Intitulé rubrique"].isin(
            selected_rubriques)]
    if selected_chapitre != []:
        filtered_df = filtered_df[filtered_df["Intitulé chapitre"].isin(
            selected_chapitre)]

    return filtered_df


def filter_votes(votes_table: pd.DataFrame,
                 persons_table: pd.DataFrame,
                 selected_parties: list[str],
                 selected_genre: list[str]) -> pd.DataFrame:
    """
    Filter the individual votes table based on the deputees.
    """

    filtered_df = persons_table.copy()

    if selected_parties != []:
        filtered_df = filtered_df[filtered_df["person_party_fr"].isin(
            selected_parties)]
    if selected_genre != []:
        filtered_df = filtered_df[filtered_df["person_gender"].isin(
            selected_genre)]

    return votes_table[votes_table["vote_person_external_id"].isin(filtered_df["person_external_id"])]


def create_table_to_plot(voting_table: pd.DataFrame,
                         votes_table: pd.DataFrame,
                         column_for_title: str = "voting_title_fr"  # "voting_external_id"
                         ) -> pd.DataFrame:
    """
    Function to merge and pivot voting and vote tables.
    """
    full_table = voting_table.merge(votes_table,
                                    left_on="voting_external_id",
                                    right_on="vote_voting_external_id")
    short_test = full_table.sort_values(by="voting_date").loc[:, [
        column_for_title, "vote_person_fullname", "vote_label"]]
    table_to_plot = short_test.pivot(columns=column_for_title,
                                     index="vote_person_fullname",
                                     values="vote_label")
    table_to_plot = table_to_plot.reset_index()
    table_to_plot = table_to_plot.rename(
        columns={'vote_person_fullname': 'Député.e'})

    return table_to_plot


if __name__ == '__main__':
    import os
    VOTING_CSV = os.path.join(os.path.dirname(
        __file__), '..', 'outputs', 'pl_voting_clean.csv')
    pl_voting_clean = pd.read_csv(VOTING_CSV)
    pl_voting_clean["voting_date"] = pd.to_datetime(
        pl_voting_clean["voting_date"])

    datesss = (datetime.date(2023, 5, 11), datetime.date(2025, 1, 31))
    print(filter_voting(voting_table=pl_voting_clean,
                        selected_rubriques=[],
                        selected_dates=datesss
                        ))
