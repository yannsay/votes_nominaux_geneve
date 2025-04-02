import streamlit as st

st.set_page_config(
    page_title = "Votes nominaux du Grand Conseil de Genève",
    page_icon =":envelope_with_arrow:", 
)

st.write("# Votes nominaux du Grand Conseil de Genève")

st.markdown(
    """
    Cette application a pour but de filtrer les votes personnels des députés du Grand Conseil de Genève.
    Elle permet de filtrer les projets de lois par:
    - Rubriques et chapitres du Registre Systématique de Genève,
    - Parti politique des député.e.s
    - Genre des député.e.s

    La base de données a été récupérée avec le project Open Parl Data. 
    L'application couvre les votes de la législature actuelle (2023-2028), du 11 mai 2023 au 15 février 2025 (dernières de date de récupération des données)
    
    Il y a uniquement les projets de loi avec un code du Registre Systématique projets de loi.
    
    - 82 votations 
    - 124 député.e.s
    - 7’568 votes nominaux

    Source: [OpenParlData](https://gitlab.com/opendata.ch/openparldatach)

"""
)