import streamlit as st
import pandas as pd
from datetime import datetime
from great_tables import GT, html
import plotly.graph_objects as go


st.title('Vote nominaux du Grand Conseil de Genève')

# DATE_COLUMN = 'date/time'
VOTING_CSV = ('outputs/pl_voting_clean.csv')
VOTES_CSV = ('outputs/clean_votes.csv')
RSGE_CSV = ("outputs/reformatted_rsge.csv")

@st.cache_data
def load_data(csv_path):
    data = pd.read_csv(csv_path)
    return data

pl_voting_clean = load_data(VOTING_CSV)
pl_voting_clean["voting_date"] = pd.to_datetime(pl_voting_clean["voting_date"])

clean_votes = load_data(VOTES_CSV)
rsge = load_data(RSGE_CSV)
rubriques_rsge = rsge[["Rubrique", "Intitulé rubrique"]].drop_duplicates(["Rubrique", "Intitulé rubrique"]).sort_values(by=["Rubrique"])

def filter_dataset():
    min_date = pl_voting_clean["voting_date"].min()
    max_date = pl_voting_clean["voting_date"].max()
    
    st.sidebar.header("Filters")
    selected_dates: tuple[datetime.date] = st.sidebar.date_input("Select dates", [min_date, max_date], min_value=min_date, max_value=max_date)
    # print(selected_dates)
    selected_dates: tuple[datetime.datetime] = (pd.to_datetime(selected_dates[0]), pd.to_datetime(selected_dates[1]))
    # print(selected_dates)


    selected_rubriques: list[str] = st.sidebar.multiselect("Selectionnez les rubriques", 
                                                           options=rubriques_rsge["Intitulé rubrique"])
    # rubrique_names: list[str] = pl_voting_clean["Rubrique"].unique()
    # rubrique_names.sort()
    # selected_chapitre: list[str] = st.sidebar.multiselect("Selectionnez les chapitres", 
    #                                                     options=)
    chapitre_names = pl_voting_clean.loc[pl_voting_clean["Intitulé rubrique"].isin(selected_rubriques)]["Intitulé chapitre"].unique()
    selected_chapitre: list[str] = st.sidebar.multiselect("Selectionnez les chapitres", 
                                                         options=chapitre_names)
    filtered_df = pl_voting_clean.copy()
    try:
        filtered_df = filtered_df[filtered_df["voting_date"].between(selected_dates[0], selected_dates[1])]

    except:
        st.error("Please select start date and end date")
        return
    
    # st.dataframe(filtered_df)
    # selected_rubriques
    # print(selected_rubriques)
    # print(type(selected_rubriques))

    if selected_rubriques != []:
        filtered_df = filtered_df[filtered_df["Intitulé rubrique"].isin(selected_rubriques)]
    if selected_chapitre != []:
        filtered_df = filtered_df[filtered_df["Intitulé chapitre"].isin(selected_chapitre)]

    # pl_voting_clean_chapitre = filtered_df["Intitulé chapitre"].unique()

    # if selected_chapitre != []:
    #     filtered_df = filtered_df[filtered_df["Intitulé chapitre"].isin(pl_voting_clean_chapitre)]
      
    full_table = filtered_df.merge(clean_votes, left_on = "voting_external_id", right_on="vote_voting_external_id")

    # st.dataframe(filtered_df)
    short_test = full_table.sort_values(by = "voting_date").loc[:,["voting_external_id", "vote_person_fullname", "vote_vote"]]
    table_to_plot = short_test.pivot(columns = "voting_external_id", index = "vote_person_fullname", values = "vote_vote")
    table_to_plot = table_to_plot.reset_index()  
    table_to_plot = table_to_plot.rename(columns={'vote_person_fullname': 'Député'})

    votes_columns = table_to_plot.columns[1:]
    # table_to_plot.index.names =["Député"]
    st.dataframe(table_to_plot)

    
    def color_picker(value: str, palette: dict[str]) -> tuple[str]:
        if "no_color" not in palette.keys():
            raise ValueError("No no_color in the palette")
        if value in palette.keys():
            return(palette[value])
        return(palette["no_color"])
    palette_votes :dict[str,str] = {"yes":"rgb(0, 77, 64)",
                                    "no":"rgb(216, 27, 96)",
                                    "abstention":"rgb(255, 193, 7)",
                                    "no_color":"rgb(245, 245, 245)"}
    cell_colors = []
    for column in table_to_plot.transpose().values.tolist():
        cell_colors.append([color_picker(value, palette_votes) for value in column])

    
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(table_to_plot.columns),
                    align='left'),
        cells=dict(values=table_to_plot.transpose().values.tolist(),
                fill = dict(color=cell_colors),
                align='left',
                font = dict(color=['black'], size=12),
    ))
    ])
    st.plotly_chart(fig)
    return (
        # GT(table_to_plot)
        # .data_color(
        #     # columns=votes_columns,
        #     palette=["#004D40","#D81B60", "#FFC107"],
        #     domain = ["yes","no", "abstention"],
        #     na_color = "white"
        #     )
        # .tab_header(
        #     title="Solar Zenith Angles from 05:30 to 12:00",
        #     subtitle=html("Average monthly values at latitude of 20&deg;N."),
        # )
        # .sub_missing(missing_text="")
    )

# filter_dataset()
st.title("Great Tables shown in Streamlit")
# st.write(filter_dataset().as_raw_html(), unsafe_allow_html=True)
filter_dataset()