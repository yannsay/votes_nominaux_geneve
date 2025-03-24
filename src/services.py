import datetime
import pandas as pd
import streamlit as st

def filter_voting(voting_table: pd.DataFrame,
                  selected_rubriques: list[str], 
                  selected_chapitre: list[str],
                  selected_dates: tuple[datetime.date]) -> pd.DataFrame:
    
    selected_dates: tuple[datetime.datetime] = (pd.to_datetime(selected_dates[0]), pd.to_datetime(selected_dates[1]))

    filtered_df = voting_table.copy()
    try:
        filtered_df = filtered_df[filtered_df["voting_date"].between(selected_dates[0], selected_dates[1],inclusive="both")]

    except:
        st.error("Please select start date and end date")
        return

    if selected_rubriques != []:
        filtered_df = filtered_df[filtered_df["Intitulé rubrique"].isin(selected_rubriques)]
    if selected_chapitre != []:
        filtered_df = filtered_df[filtered_df["Intitulé chapitre"].isin(selected_chapitre)]

    return filtered_df

    
if __name__ == '__main__':
    import os
    VOTING_CSV = os.path.join(os.path.dirname( __file__ ), '..','outputs', 'pl_voting_clean.csv')
    pl_voting_clean = pd.read_csv(VOTING_CSV)
    pl_voting_clean["voting_date"] = pd.to_datetime(pl_voting_clean["voting_date"])

    datesss = (datetime.date(2023, 5, 11), datetime.date(2025, 1, 31))
    print(filter_voting(voting_table =  pl_voting_clean,
                    selected_rubriques = [], 
                    selected_dates = datesss
                                   ))