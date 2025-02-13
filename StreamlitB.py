import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu
import requests
from bs4 import BeautifulSoup
import streamlit.components.v1 as components
import base64
import os

from utils2 import lien_google
from utils3 import category
from utils4 import api
from utils5 import transfo_liste
from utils6 import carte
from utils8 import fond  # Importation de la fonction fond()
from utils10 import autoplay_audio
# Importation de utils8bis.py pour l'image de fond
from utils8bis import fond
# Le chemin vers le fichier audio téléchargé
audio_file_path = "Robin Schulz - Sugar (Official Instrumental).mp3"
# ========== 🔹 Configuration de la Sidebar 🔹 ==========
with st.sidebar:
    #fond("Rue6.jpg")
    st.write("bonjour")
    autoplay_audio(audio_file_path)
    selection = option_menu(
        menu_title=None,
        options=["Accueil", "Recherche par département", "Recherche par ville"],
        icons=["house", "map", "shop"],
        menu_icon="cast",
        default_index=0
    )

# ========== 🔹 Page d'Accueil 🔹 ==========
if selection == "Accueil":
    st.markdown("## 🎉 Bienvenue sur notre application !")
    
    # 🖼️ Afficher une image ou GIF de bienvenue
    file_path = "AAAaccueiltest.gif"
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            contents = file.read()
            data_url = base64.b64encode(contents).decode("utf-8")
        st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="Accueil GIF">', unsafe_allow_html=True)
    else:
        st.warning("⚠️ GIF d'accueil non trouvé ! Vérifiez 'AAAaccueiltest.gif'.")

    st.write("Recommandations personnalisées de restaurants par Aurélie, Anissa et Anaëlle. 👨‍🍳👩‍🍳👨‍🍳")

# ========== 🔹 Recherche par Département 🔹 ==========
elif selection == "Recherche par département":
    st.markdown("## 🔍 Trouver un restaurant par département")

    # Charger les données
    df_loc1 = pd.read_csv('df_loc.csv')
    departements_uniques = sorted(set(df_loc1["nom_departement"].unique()).union(set(df_loc1["department_code"].astype(str).unique())))

    # Sélection du département
    selected_department = st.selectbox("Sélectionnez un département :", departements_uniques)

    # Filtrage des villes du département sélectionné
    filtered_df = df_loc1[df_loc1["nom_departement"] == selected_department]
    selected_city = st.selectbox("Sélectionnez une ville :", filtered_df["nom_ville"].unique().tolist())

    st.write(f"📍 **Vous avez sélectionné :** {selected_city}, {selected_department}")

# ========== 🔹 Recherche par Ville 🔹 ==========
elif selection == "Recherche par ville":
    st.markdown("## 🔎 Trouver un restaurant par ville")

    df_loc1 = pd.read_csv('df_loc.csv')
    selected_city = st.selectbox("Sélectionnez une ville :", sorted(df_loc1["nom_ville"].unique().tolist()))

    available_departments = df_loc1[df_loc1["nom_ville"] == selected_city][["nom_departement", "department_code"]].drop_duplicates()

    if not available_departments.empty:
        selected_department_row = st.selectbox("Sélectionnez le département :", available_departments["nom_departement"].unique().tolist())
        department_code = available_departments[available_departments["nom_departement"] == selected_department_row]["department_code"].values[0]

        st.write(f"📍 **Ville sélectionnée :** {selected_city}")
        st.write(f"🏛️ **Département :** {selected_department_row} ({department_code})")
    else:
        st.warning("⚠️ Aucune correspondance trouvée pour cette ville.")
