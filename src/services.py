"""Functions for the application"""
import datetime
import pandas as pd
import streamlit as st
from great_tables import GT

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
                 selected_persons: list[str],
                 selected_parties: list[str],
                 selected_genre: list[str]) -> pd.DataFrame:
    """
    Filter the individual votes table based on the deputees.
    """

    filtered_df = persons_table.copy()
    if selected_persons != []:
        filtered_df = filtered_df[filtered_df["person_fullname"].isin(
            selected_persons)]
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


def plot_votes(data_to_plot: pd.DataFrame) -> str:
    votes_columns = data_to_plot.columns[1:].to_list()
    return (GT(data_to_plot)\
        .data_color(
            columns=votes_columns,
            palette=["#004D40", "#D81B60", "#FFC107"],
            domain=["Oui", "Non", "Abstention"],
            na_color="white"
        ).as_raw_html())

def plot_voting(data_to_plot: pd.DataFrame, links_column: str) -> str:
    data_to_plot[links_column] = "[" + data_to_plot[links_column] + "](" + data_to_plot[links_column] + ")"
    # votes_columns = data_to_plot.columns[1:].to_list()
    return (
        GT(data_to_plot)
        .fmt_markdown(columns=links_column)
        .cols_width(
            cases={
                links_column: "10%"
            }).as_raw_html()
    )

def create_info_table(voting_table: pd.DataFrame,
                      data_to_plot: pd.DataFrame) -> pd.DataFrame:
    filtered_voting = voting_table.copy()
    filtered_voting = filtered_voting[filtered_voting["voting_title_fr"].isin(
        data_to_plot.columns)]
    filtered_voting["lien_grand_conseil"] = "https://ge.ch/grandconseil/m/search?search=" + \
        filtered_voting["voting_title_fr"]
    filtered_voting["lien_grand_conseil"] = filtered_voting["lien_grand_conseil"].str.replace(
        " ", "%20")
    columns_to_keep = ["voting_affair_number", "voting_date", "voting_title_fr", "voting_affair_title_fr", "lien_grand_conseil", "voting_results_yes",
                       "voting_results_no", "voting_results_abstention", "type_vote", "Référence", "Intitulé rubrique", "Intitulé chapitre", "Intitulé"]
    clean_voting = filtered_voting.loc[:, columns_to_keep]

    dictionnaire_name = {"voting_affair_number": "Identifiant affaire",
                         "voting_date": "Date du vote",
                         "voting_title_fr": "Titre du vote",
                         "voting_affair_title_fr": "Titre affaire",
                         "lien_grand_conseil": "Lien Grand Conseil",
                         "voting_results_yes": "Résultat - Oui",
                         "voting_results_no": "Résutlat - Non",
                         "voting_results_abstention": "Résultat - Abstention",
                         "type_vote": "Type de vote", }
    clean_voting = clean_voting.rename(columns=dictionnaire_name)
    clean_voting = clean_voting.reset_index()
    clean_voting = clean_voting.drop(columns="index")

    return clean_voting


    