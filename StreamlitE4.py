import streamlit as st
import pandas as pd
import requests
import warnings
from bs4 import BeautifulSoup
import requests
import pandas as pd
from utils1 import enlever_accents
from utils2 import lien_google
from utils3 import category
from utils4 import api

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

        # Entrée un nombre de metres de distance de la ville
        #distance = st.number_input("Entrez un nombre de mètres :")
        distance = st.slider("Sélectionnez la plage de date :",
           min_value=0,
           max_value=40000,
           value=40000
          )
        

        # Rechercher des restaurants via l'API Yelp
        df = api(selected_city)

                   
            # Filtrage pour inclure uniquement les restaurants en France
        df_in_france = df[df['location.country']== "FR"]
        df_in_france = df[df['distance']<distance]
        df_in_france = df_in_france.reset_index(drop = True)
        st.write(df_in_france)

        st.write(f"Restaurants trouvés à {selected_city}, {selected_department} (France):")
        if not df_in_france.empty:
            st.write(f"Restaurants trouvés à {selected_city}, {selected_department} (France):")
            
    for index, row in df_in_france.iterrows():
        name = row["name"]
        address = ", ".join(row["location.display_address"])  # Si c'est une liste, on la joint en chaîne
        rating = row["rating"]
        review_count = row["review_count"]
        image_url = row["image_url"]
        phone = row["display_phone"]
        lienG = lien_google(name, row["location.city"])  # Générer le lien Google

        st.write(f"- **{name}**")
        if image_url:
            st.image(image_url, width=150)
        else:
            st.image("poster.png", width=150)
        
        st.write(f"  - Adresse : {address}")
        st.write(f"  - Note : {rating} ⭐")
        st.write(f"  - Nb Vote : {review_count}")
        st.write(f"  - Téléphone : {phone}")
        st.write(lienG)
        st.write("---")

else:
    st.write("Aucun restaurant trouvé pour cette ville.")