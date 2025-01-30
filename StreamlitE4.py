import streamlit as st
import pandas as pd
import warnings
from bs4 import BeautifulSoup
import requests
import pandas as pd
import ast 
import folium
from streamlit_folium import st_folium


from utils1 import enlever_accents
from utils2 import lien_google
from utils3 import category
from utils4 import api
from utils5 import transfo_liste
from utils6 import carte
from utils7 import geocode


warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Charger le fichier CSV contenant les départements et villes
df_loc1 = pd.read_csv('df_loc.csv')

# Normaliser les colonnes pour la recherche insensible aux accents
df_loc1["nom_departement_normalise"] = df_loc1["nom_departement"].apply(enlever_accents).str.lower()
df_loc1["nom_ville_normalise"] = df_loc1["nom_ville"].apply(enlever_accents).str.lower()


# Titre de l'application
st.title("Recherche de département, ville et restaurants en France")
st.image('titre.png', width=300)

# Entrée pour rechercher un département par nom ou numéro
query = st.text_input("Entrez le nom ou le numéro du département :").lower()

# Afficher les suggestions seulement si une requête a été saisie
if query.strip():  # Vérifie si la requête n'est pas vide ou composée uniquement d'espaces
    query_normalise = enlever_accents(query)  # Normaliser la requête

    # Filtrer les départements correspondant à la requête
    filtered_departments = df_loc1[
        df_loc1["nom_departement_normalise"].str.contains(query_normalise) |
        df_loc1["department_code"].str.contains(query)
    ]

    if not filtered_departments.empty:
        # Proposer les départements filtrés
        selected_department = st.selectbox(
            "Sélectionnez un département parmi les suggestions :",
            options=filtered_departments["nom_departement"].unique()
        )

        # Filtrer les villes du département sélectionné
        filtered_cities = df_loc1[df_loc1["nom_departement"] == selected_department]["nom_ville"].unique()

        # Proposer les villes associées
        selected_city = st.selectbox(
            "Sélectionnez une ville parmi les suggestions :",
            options=filtered_cities
        )

        # Résultat final
        st.write(f"Vous avez sélectionné le département : {selected_department}")
        st.write(f"Et la ville : {selected_city}")

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
                st.write(f"**Restaurants correspondant à votre sélection :**")
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
