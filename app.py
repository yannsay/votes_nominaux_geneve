import streamlit as st

readme_page = st.Page("app_pages/presentation.py", 
                      title="Présentation")
projets_de_lois_page = st.Page("app_pages/projets_de_lois.py", 
                      title="Par projets de loi")
pg = st.navigation([readme_page, projets_de_lois_page])
pg.run()