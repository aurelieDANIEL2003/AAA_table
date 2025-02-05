import streamlit as st
import pandas as pd
import unidecode
import ast 
import folium
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu

from utils1 import enlever_accents
from utils2 import lien_google
from utils3 import category
from utils4 import api
from utils5 import transfo_liste
from utils6 import carte
from utils7 import geocode

# Charger les données (remplace par ton fichier réel)
df_loc1 = pd.read_csv('df_loc.csv')

# Ajouter des colonnes normalisées pour la recherche
df_loc1["nom_departement_normalise"] = df_loc1["nom_departement"].apply(enlever_accents)
df_loc1["nom_ville_normalise"] = df_loc1["nom_ville"].apply(enlever_accents)
df_loc1["department_code_normalise"] = df_loc1["department_code"].apply(enlever_accents)

# Menu latéral
with st.sidebar:
    selection = option_menu(
        menu_title=None,
        options=["Accueil" ,"Recherche par département", "Recherche par ville"],
        icons=["house", "map", "shop",],
        menu_icon="cast",
        default_index=0
    )

   
# Page d'accueil
if selection == "Accueil":
    st.title('AAA table! 🍽️')
    st.image('titre.png', width=500)
    st.write("""
        Recommandations personnalisées de Restaurants Made by Aurélie, Anissa et Anaëlle. 👨‍🍳👨‍🍳👨‍🍳
    """)


# **Mode 1 : Sélection d'un département (nom ou numéro), puis d'une ville**

if selection == "Recherche par département":
    # Sélection du département ou du numéro
    selected_department = st.selectbox(
        "Sélectionnez un département (nom ou numéro) :",
        options=df_loc1["nom_departement_normalise"].unique().tolist() + df_loc1["department_code_normalise"].unique().tolist()
    )
    

    # Identifier le département correspondant
    if selected_department in df_loc1["department_code_normalise"].values:
        filtered_df = df_loc1[df_loc1["department_code_normalise"] == selected_department]
    else:
        filtered_df = df_loc1[df_loc1["nom_departement_normalise"] == selected_department]
   
    # Sélection de la ville dans le département choisi
    selected_city = st.selectbox(
        "Sélectionnez une ville dans ce département :",
        options=filtered_df["nom_ville_normalise"].unique().tolist()
    )

    # Affichage des résultats
    department_name = filtered_df["nom_departement_normalise"].iloc[0]
    department_code = filtered_df["department_code_normalise"].iloc[0]
    
    st.write(f"### Département : {department_name} ({department_code})")
    st.write(f"### Ville sélectionnée : {selected_city}")

    try:
        df = api(selected_city)


        # Entrée un nombre de metres de distance de la ville
        distance = st.slider("Sélectionnez une distance en mètres :",
        min_value=0,
        max_value=40000,
        value=40000
        )
        
        
                
            # Filtrage pour inclure uniquement les restaurants en France
        df = df.drop(columns=['alias', 'transactions', 'phone', 'location.address2', 'price', 
    'location.address3', 'location.zip_code', 'attributes.business_temp_closed', 'attributes.open24_hours', 'attributes.waitlist_reservation'])
        df_in_france = df[df['location.country']== "FR"]
        df_in_france = df_in_france[df_in_france['distance']<distance]
        df_in_france = df_in_france.reset_index(drop = True)

        

        liste = transfo_liste(df_in_france['categories'])
        df_in_france['categories'] = df_in_france['categories'].apply(category) 
        toutes_les_categories = set()
        for categorie in df_in_france['categories']:
                toutes_les_categories.update(categorie)
                
            
        toutes_les_categories = list(toutes_les_categories)
        # on choisit ce que l'on veut manger
        cat_choisie = st.multiselect("Que voulez vous manger?", options = sorted(toutes_les_categories))

        # Vérifier que l'utilisateur a choisi au moins une catégorie
        if cat_choisie:
        # Filtrage des restaurants qui contiennent au moins une des catégories choisies
            df_filtered = df_in_france[df_in_france['categories'].apply(lambda x: any(cat in x for cat in cat_choisie))]
        else:
            df_filtered = df_in_france  # Si aucune catégorie sélectionnée, afficher tout

        

        # Affichage des résultats filtrés
        if not df_filtered.empty:
            st.write(f"**🍴Restaurants correspondant à votre sélection :**")
            affiche_carte = st.toggle("Veux tu la carte", value=True)
            if affiche_carte:
                m = carte(df_filtered, selected_city)
                st_data = st_folium(m, width=725)


            for _, row in df_filtered.iterrows():
                name = row["name"]
                address = ", ".join(row.get("location.display_address", []))  
                rating = row.get("rating", "N/A")
                review_count = row.get("review_count", 0)
                image_url = row.get("image_url", "")
                phone = row.get("display_phone", "Non disponible")
                lienG = lien_google(name, row["location.city"])  # Générer le lien Google

                st.write(f"- **{name}**")
                if image_url:
                    st.image(image_url, width=150)
                else:
                    st.image("poster.png", width=150)

                st.write(f"  - 📍 Adresse : {address}")
                st.write(f"  - ⭐ Note : {rating} / 5")
                st.write(f"  - 🗳️ Nombre d'avis : {review_count}")
                st.write(f"  - 📞 Téléphone : {phone}")
                st.write(f"  - 🔍 Lien : {lienG}")
                st.write("---")

        else:
            st.write("Aucun restaurant trouvé pour ces catégories.")

    except :
        st.write("aucun restaurant trouvé pour cette ville, veuillez choisir une autre ville")


# **Mode 2 : Sélection d'une ville directement, puis choix du département**
elif selection == "Recherche par ville":
    # Sélection de la ville
    selected_city = st.selectbox(
        "Sélectionnez une ville :",
        options=df_loc1["nom_ville_normalise"].unique().tolist()
    )

    # Trouver tous les départements où cette ville est présente
    available_departments = df_loc1[df_loc1["nom_ville_normalise"] == selected_city][["nom_departement_normalise", "department_code_normalise"]].drop_duplicates()

    # Sélection du département où cette ville est située
    selected_department_row = st.selectbox(
        "Sélectionnez le département où cette ville est présente :",
        options=available_departments["nom_departement_normalise"].unique().tolist()
    )

    # Récupérer le code du département sélectionné
    department_code = available_departments[available_departments["nom_departement_normalise"] == selected_department_row]["department_code_normalise"].values[0]

    # Affichage des résultats
    st.write(f"### Ville sélectionnée : {selected_city}")
    st.write(f"### Département : {selected_department_row} ({department_code})")
# verification que la ville selectionnée est dans l'API
    try:
        df = api(selected_city)


        # Entrée un nombre de metres de distance de la ville
        distance = st.slider("Sélectionnez une distance en mètres :",
        min_value=0,
        max_value=40000,
        value=40000
        )
        
        
                
            # Filtrage pour inclure uniquement les restaurants en France
        df = df.drop(columns=['alias', 'transactions', 'phone', 'location.address2', 'price', 
    'location.address3', 'location.zip_code', 'attributes.business_temp_closed', 'attributes.open24_hours', 'attributes.waitlist_reservation'])
        df_in_france = df[df['location.country']== "FR"]
        df_in_france = df_in_france[df_in_france['distance']<distance]
        df_in_france = df_in_france.reset_index(drop = True)

        

        liste = transfo_liste(df_in_france['categories'])
        df_in_france['categories'] = df_in_france['categories'].apply(category) 
        toutes_les_categories = set()
        for categorie in df_in_france['categories']:
                toutes_les_categories.update(categorie)
                
            
        toutes_les_categories = list(toutes_les_categories)
        # on choisit ce que l'on veut manger
        cat_choisie = st.multiselect("Que voulez vous manger?", options = sorted(toutes_les_categories))

        # Vérifier que l'utilisateur a choisi au moins une catégorie
        if cat_choisie:
        # Filtrage des restaurants qui contiennent au moins une des catégories choisies
            df_filtered = df_in_france[df_in_france['categories'].apply(lambda x: any(cat in x for cat in cat_choisie))]
        else:
            df_filtered = df_in_france  # Si aucune catégorie sélectionnée, afficher tout

        

        # Affichage des résultats filtrés
        if not df_filtered.empty:
            st.write(f"**🍴Restaurants correspondant à votre sélection :**")
            affiche_carte = st.toggle("Veux tu la carte", value=True)
            if affiche_carte:
                m = carte(df_filtered, selected_city)
                st_data = st_folium(m, width=725)


            for _, row in df_filtered.iterrows():
                name = row["name"]
                address = ", ".join(row.get("location.display_address", []))  
                rating = row.get("rating", "N/A")
                review_count = row.get("review_count", 0)
                image_url = row.get("image_url", "")
                phone = row.get("display_phone", "Non disponible")
                lienG = lien_google(name, row["location.city"])  # Générer le lien Google

                st.write(f"- **{name}**")
                if image_url:
                    st.image(image_url, width=150)
                else:
                    st.image("poster.png", width=150)

                st.write(f"  - 📍 Adresse : {address}")
                st.write(f"  - ⭐ Note : {rating} / 5")
                st.write(f"  - 🗳️ Nombre d'avis : {review_count}")
                st.write(f"  - 📞 Téléphone : {phone}")
                st.write(f"  - 🔍 Lien : {lienG}")
                st.write("---")

        else:
            st.write("Aucun restaurant trouvé pour ces catégories.")

    except :
        st.write("aucun restaurant trouvé pour cette ville, veuillez choisir une autre ville")
