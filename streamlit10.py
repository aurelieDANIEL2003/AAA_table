# ✅ Menu latéral avec indentation corrigée

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
from utils8bis import fond  # Importation de la fonction fond()
from utils10 import autoplay_audio

# Définition du User-Agent pour éviter d'être bloqué par les navigateurs
#navigator = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'

# Le chemin vers le fichier audio téléchargé
audio_file_path = "Musique_aaatable.mp3"

# Charger les données des départements et villes
df_loc1 = pd.read_csv('df_loc.csv')

# Nettoyage et mise en forme des noms de département
df_loc1["nom_departement_lower"] = df_loc1["nom_departement"].astype(str).str.lower().str.strip()
df_loc1["department_code_lower"] = df_loc1["department_code"].astype(str).str.strip()

# Liste unique des départements (noms + codes)
departements_uniques = sorted(set(df_loc1["nom_departement"].unique()).union(set(df_loc1["department_code"].astype(str).unique())))

# Menu latéral
# ✅ Menu latéral
with st.sidebar:
    selection = option_menu(
        menu_title=None,
        options=["Accueil", "Recherche par département", "Recherche par ville"],
        icons=["house", "map", "shop"],
        menu_icon="cast",
        default_index=0
    )

    # ✅ Nom de l’image corrigé
    side_bg = "Rue66.jpg"  # Nom du fichier
    side_bg_path = os.path.abspath(side_bg)

    # ✅ Vérification de l’image
    os.path.exists(side_bg_path)
    st.write(f"✅ Image trouvée : {side_bg_path}")
    fond(side_bg_path)


    # ✅ Vérification de l’audio
    audio_file_path = "Musique_aaatable.mp3"
    os.path.exists(audio_file_path)
    autoplay_audio(audio_file_path)
    #else:
    #   st.error(f"❌ Audio introuvable : {audio_file_path}")

    # ✅ Debugging
    st.write(f"🔍 Chemin absolu : {side_bg_path}")
    #st.write(f"📂 Fichier trouvé ? {'✅ Oui' if os.path.exists(side_bg_path) else '❌ Non'}")





# ✅ Mode 1 : Recherche par département
if selection == "Recherche par département":
    selected_department_original = st.selectbox("Sélectionnez un département :", departements_uniques)

    if selected_department_original in df_loc1["department_code"].astype(str).values:
        filtered_df = df_loc1[df_loc1["department_code"].astype(str) == selected_department_original]
    else:
        filtered_df = df_loc1[df_loc1["nom_departement"] == selected_department_original]

    selected_city = st.selectbox("Sélectionnez une ville :", filtered_df["nom_ville"].unique().tolist())
    st.write(f"A {selected_city}, {filtered_df['nom_departement'].iloc[0]} ({filtered_df['department_code'].iloc[0]})")

    try:
        df = api(selected_city)

        if df.empty:
            st.warning("⚠️ Aucun restaurant trouvé.")
        else:
            distance = st.slider("Distance (mètres) :", 0, 40000, 40000)
            df_in_france = df[df['location.country'] == "FR"]
            df_in_france = df_in_france[df_in_france['distance'] < distance].reset_index(drop=True)

            if df_in_france.empty:
                st.warning("⚠️ Aucun restaurant à cette distance.")
            else:
                df_in_france['categories'] = df_in_france['categories'].apply(category)
                toutes_les_categories = sorted(
                    set(cat for liste in df_in_france['categories'] for cat in liste)
                )

                cat_choisie = st.multiselect("Que voulez-vous manger ?", options=toutes_les_categories)
                df_filtered = df_in_france[df_in_france['categories'].apply(
                    lambda x: any(cat in x for cat in cat_choisie)
                )] if cat_choisie else df_in_france

                if not df_filtered.empty:
                    st.write("🍴 **Restaurants disponibles :**")
                    if st.toggle("Afficher la carte", value=True):
                        st_folium(carte(df_filtered, selected_city), width=725)

                    for _, row in df_filtered.iterrows():
                        st.write(f"- **{row['name']}**")
                        st.image(row["image_url"] if row["image_url"] else "poster.png", width=150)
                        st.write(f"📍 {', '.join(row['location.display_address'])}")
                        st.write(f"⭐ {row['rating']} / 5 ({row['review_count']} avis)")
                        st.write(f"📞 {row['display_phone'] or 'Non disponible'}")
                        st.write(f"🔍 [Voir sur Google]({lien_google(row['name'], row['location.city'])})")
                        st.write("---")
    except Exception as e:
        st.error(f"Erreur : {str(e)}")

# ✅ Mode 2 : Recherche par ville
elif selection == "Recherche par ville":
    selected_city = st.selectbox(
        "Sélectionnez une ville :",
        sorted(df_loc1["nom_ville"].unique().tolist())
    )

    available_departments = df_loc1[
        df_loc1["nom_ville"] == selected_city
    ][["nom_departement", "department_code"]].drop_duplicates()

    if not available_departments.empty:
        selected_department_row = st.selectbox(
            "Sélectionnez le département :",
            available_departments["nom_departement"].unique().tolist()
        )
        department_code = available_departments[
            available_departments["nom_departement"] == selected_department_row
        ]["department_code"].values[0]

        st.write(f"### Ville sélectionnée : {selected_city}")
        st.write(f"### Département : {selected_department_row} ({department_code})")

        try:
            df = api(selected_city)
            if df.empty:
                st.warning("⚠️ Aucun restaurant trouvé.")
            else:
                distance = st.slider("Distance (mètres) :", 0, 40000, 40000)
                df_in_france = df[df['location.country'] == "FR"]
                df_in_france = df_in_france[df_in_france['distance'] < distance].reset_index(drop=True)

                if df_in_france.empty:
                    st.warning("⚠️ Aucun restaurant à cette distance.")
                else:
                    df_in_france['categories'] = df_in_france['categories'].apply(category)
                    toutes_les_categories = sorted(
                        set(cat for liste in df_in_france['categories'] for cat in liste)
                    )

                    cat_choisie = st.multiselect(
                        "Que voulez-vous manger ?", options=toutes_les_categories
                    )
                    df_filtered = df_in_france[df_in_france['categories'].apply(
                        lambda x: any(cat in x for cat in cat_choisie)
                    )] if cat_choisie else df_in_france

                    if not df_filtered.empty:
                        st.write("🍴 **Restaurants disponibles :**")
                        if st.toggle("Afficher la carte", value=True):
                            st_folium(carte(df_filtered, selected_city), width=725)

                        for _, row in df_filtered.iterrows():
                            st.write(f"- **{row['name']}**")
                            st.image(
                                row["image_url"] if row["image_url"] else "poster.png",
                                width=150
                            )
                            st.write(f"📍 {', '.join(row['location.display_address'])}")
                            st.write(f"⭐ {row['rating']} / 5 ({row['review_count']} avis)")
                            st.write(f"📞 {row['display_phone'] or 'Non disponible'}")
                            st.write(f"🔍 [Voir sur Google]({lien_google(row['name'], row['location.city'])})")
                            st.write("---")
        except Exception as e:
            st.error(f"Erreur : {str(e)}")
    else:
        st.warning("⚠️ Aucune correspondance trouvée pour cette ville.")
