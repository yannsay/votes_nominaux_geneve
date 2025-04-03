import streamlit as st

readme_page = st.Page("app_pages/presentation.py", 
                      title="Présentation")
projets_de_lois_page = st.Page("app_pages/projets_de_lois.py", 
                      title="Par projets de loi - Registre Sytématique genevois")
autres_votes_page = st.Page("app_pages/autres_votes.py", 
                      title="Autres votes")
pg = st.navigation([readme_page, projets_de_lois_page, autres_votes_page])
pg.run()