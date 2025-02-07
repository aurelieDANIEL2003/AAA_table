import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu
import requests
from bs4 import BeautifulSoup
import streamlit as st
import base64

from utils2 import lien_google
from utils3 import category
from utils4 import api
from utils5 import transfo_liste
from utils6 import carte
from utils8 import fond  # Importation de la fonction fond()

# Définition du User-Agent pour éviter d'être bloqué par les navigateurs
#navigator = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'

# Charger les données des départements et villes
df_loc1 = pd.read_csv('df_loc.csv')

# Nettoyage et mise en forme des noms de département
df_loc1["nom_departement_lower"] = df_loc1["nom_departement"].astype(str).str.lower().str.strip()
df_loc1["department_code_lower"] = df_loc1["department_code"].astype(str).str.strip()

# Liste unique des départements (noms + codes)
departements_uniques = sorted(set(df_loc1["nom_departement"].unique()).union(set(df_loc1["department_code"].astype(str).unique())))

# Appliquer le fond d'écran
fond("fondR.jpg") 

# Menu latéral
with st.sidebar:
    selection = option_menu(
        menu_title=None,
        options=["Accueil", "Recherche par département", "Recherche par ville"],
        icons=["house", "map", "shop"],
        menu_icon="cast",
        default_index=0
    )

# **Page d'accueil**
if selection == "Accueil":
    st.title('AAA table! 🍽️')
    st.image('titre.png', width=500)
    st.write("Recommandations personnalisées de Restaurants Made by Aurélie, Anissa et Anaëlle. 👨‍🍳👨‍🍳👨‍🍳")

# **Mode 1 : Recherche par département**
if selection == "Recherche par département":
    selected_department_original = st.selectbox("Sélectionnez un département :", departements_uniques)

    if selected_department_original in df_loc1["department_code"].astype(str).values:
        filtered_df = df_loc1[df_loc1["department_code"].astype(str) == selected_department_original]
    else:
        filtered_df = df_loc1[df_loc1["nom_departement"] == selected_department_original]

    selected_city = st.selectbox("Sélectionnez une ville :", filtered_df["nom_ville"].unique().tolist())

    st.write(f"### Département : {filtered_df['nom_departement'].iloc[0]} ({filtered_df['department_code'].iloc[0]})")
    st.write(f"### Ville sélectionnée : {selected_city}")

    # **Recherche de restaurants**
    try:
        df = api(selected_city)

        if df.empty:
            st.warning("⚠️ Aucun restaurant trouvé pour cette ville. Veuillez essayer une autre ville.")
        else:
            distance = st.slider("Sélectionnez une distance en mètres :", 0, 40000, 40000)
            df_in_france = df[df['location.country'] == "FR"]
            df_in_france = df_in_france[df_in_france['distance'] < distance].reset_index(drop=True)

            if df_in_france.empty:
                st.warning("⚠️ Aucun restaurant trouvé à cette distance.")
            else:
                df_in_france['categories'] = df_in_france['categories'].apply(category)
                toutes_les_categories = sorted(set(cat for liste in df_in_france['categories'] for cat in liste))

                cat_choisie = st.multiselect("Que voulez-vous manger ?", options=toutes_les_categories)
                df_filtered = df_in_france[df_in_france['categories'].apply(lambda x: any(cat in x for cat in cat_choisie))] if cat_choisie else df_in_france

                if not df_filtered.empty:
                    st.write("🍴 **Restaurants correspondant à votre sélection :**")
                    if st.toggle("Afficher la carte", value=True):
                        st_folium(carte(df_filtered, selected_city), width=725)

                    for _, row in df_filtered.iterrows():
                        st.write(f"- **{row['name']}**")
                        st.image(row["image_url"] if row["image_url"] else "poster.png", width=150)
                        st.write(f"📍 Adresse : {', '.join(row['location.display_address'])}")
                        st.write(f"⭐ Note : {row['rating']} / 5")
                        st.write(f"🗳️ Nombre d'avis : {row['review_count']}")
                        st.write(f"📞 Téléphone : {row['display_phone'] or 'Non disponible'}")
                        st.write(f"🔍 [Voir sur Google]({lien_google(row['name'], row['location.city'])})")
                        st.write("---")
    except Exception as e:
        st.error(f"Erreur lors de la récupération des restaurants : {str(e)}")

# **Mode 2 : Recherche par ville**
elif selection == "Recherche par ville":
    selected_city = st.selectbox("Sélectionnez une ville :", sorted(df_loc1["nom_ville"].unique().tolist()))

    available_departments = df_loc1[df_loc1["nom_ville"] == selected_city][["nom_departement", "department_code"]].drop_duplicates()

    if not available_departments.empty:
        selected_department_row = st.selectbox("Sélectionnez le département :", available_departments["nom_departement"].unique().tolist())
        department_code = available_departments[available_departments["nom_departement"] == selected_department_row]["department_code"].values[0]

        st.write(f"### Ville sélectionnée : {selected_city}")
        st.write(f"### Département : {selected_department_row} ({department_code})")

        try:
            df = api(selected_city)

            if df.empty:
                st.warning("⚠️ Aucun restaurant trouvé pour cette ville. Veuillez essayer une autre ville.")
            else:
                distance = st.slider("Sélectionnez une distance en mètres :", 0, 40000, 40000)
                df_in_france = df[df['location.country'] == "FR"]
                df_in_france = df_in_france[df_in_france['distance'] < distance].reset_index(drop=True)

                if df_in_france.empty:
                    st.warning("⚠️ Aucun restaurant trouvé à cette distance.")
                else:
                    df_in_france['categories'] = df_in_france['categories'].apply(category)
                    toutes_les_categories = sorted(set(cat for liste in df_in_france['categories'] for cat in liste))

                    cat_choisie = st.multiselect("Que voulez-vous manger ?", options=toutes_les_categories)
                    df_filtered = df_in_france[df_in_france['categories'].apply(lambda x: any(cat in x for cat in cat_choisie))] if cat_choisie else df_in_france

                    if not df_filtered.empty:
                        st.write("🍴 **Restaurants correspondant à votre sélection :**")
                        if st.toggle("Afficher la carte", value=True):
                            st_folium(carte(df_filtered, selected_city), width=725)

        except Exception as e:
            st.error(f"Erreur lors de la récupération des restaurants : {str(e)}")
    else:
        st.warning("⚠️ Aucune correspondance trouvée pour cette ville.")
