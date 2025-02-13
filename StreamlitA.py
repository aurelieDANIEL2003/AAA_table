import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu
import requests
from bs4 import BeautifulSoup
import base64
import os

# Importation de utils8bis.py (sans modification)
from utils8bis import fond

# Définition du User-Agent pour éviter d'être bloqué par les navigateurs
# navigator = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'

# Le chemin vers le fichier audio téléchargé
audio_file_path = "Musique_aaatable.mp3"

# Charger les données des départements et villes
df_loc1 = pd.read_csv('df_loc.csv')

# Nettoyage et mise en forme des noms de département
df_loc1["nom_departement_lower"] = df_loc1["nom_departement"].astype(str).str.lower().str.strip()
df_loc1["department_code_lower"] = df_loc1["department_code"].astype(str).str.strip()

# Liste unique des départements (noms + codes)
departements_uniques = sorted(set(df_loc1["nom_departement"].unique()).union(set(df_loc1["department_code"].astype(str).unique())))

# ======= Interface Streamlit =======

# Menu latéral
with st.sidebar:
    fond("Rue6.jpg")  # Utilisation de utils8bis pour afficher l'image de fond
    selection = option_menu(
        menu_title=None,
        options=["Accueil", "Recherche par département", "Recherche par ville"],
        icons=["house", "map", "shop"],
        menu_icon="cast",
        default_index=0
    )

# **Page d'accueil**
if selection == "Accueil":
    file = open("AAAaccueiltest.gif", "rb")
    contents = file.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file.close()

    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
        unsafe_allow_html=True,
    )
    st.write("Recommandations personnalisées de Restaurants Made by Aurélie, Anissa et Anaëlle. 👨‍🍳👨‍🍳👨‍🍳")

# **Mode 1 : Recherche par département**
elif selection == "Recherche par département":
    selected_department_original = st.selectbox("Sélectionnez un département :", departements_uniques)

    if selected_department_original in df_loc1["department_code"].astype(str).values:
        filtered_df = df_loc1[df_loc1["department_code"].astype(str) == selected_department_original]
    else:
        filtered_df = df_loc1[df_loc1["nom_departement"] == selected_department_original]

    selected_city = st.selectbox("Sélectionnez une ville :", filtered_df["nom_ville"].unique().tolist())

    st.write(f"A {selected_city}, {filtered_df['nom_departement'].iloc[0]} ({filtered_df['department_code'].iloc[0]})")

# **Mode 2 : Recherche par ville**
elif selection == "Recherche par ville":
    selected_city = st.selectbox("Sélectionnez une ville :", sorted(df_loc1["nom_ville"].unique().tolist()))

    available_departments = df_loc1[df_loc1["nom_ville"] == selected_city][["nom_departement", "department_code"]].drop_duplicates()

    if not available_departments.empty:
        selected_department_row = st.selectbox("Sélectionnez le département :", available_departments["nom_departement"].unique().tolist())
        department_code = available_departments[available_departments["nom_departement"] == selected_department_row]["department_code"].values[0]

        st.write(f"### Ville sélectionnée : {selected_city}")
        st.write(f"### Département : {selected_department_row} ({department_code})")
    else:
        st.warning("⚠️ Aucune correspondance trouvée pour cette ville.")
