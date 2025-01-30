import streamlit as st
import pandas as pd
import requests
import warnings
from bs4 import BeautifulSoup
import requests
import pandas as pd
from utils1 import enlever_accents
from utils2 import lien_google

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Charger le fichier CSV contenant les départements et villes
df_loc1 = pd.read_csv('df_loc.csv')

# Normaliser les colonnes pour la recherche insensible aux accents
df_loc1["nom_departement_normalise"] = df_loc1["nom_departement"].apply(enlever_accents).str.lower()
df_loc1["nom_ville_normalise"] = df_loc1["nom_ville"].apply(enlever_accents).str.lower()

# Clé API Yelp
API_KEY = "m2Q6PLrDbFonmYwJT-IqBq6DmYX_MhZ_DV6Gnls4JTnj0qUtuNKnaEt48q0lr9mrZM-husmMgztJc4TKF9TbChpv7nfCKU5GYKH7AxT3rtWwSJBVBtR8RfZmihaSZ3Yx"

# URL de base pour l'API Yelp
YELP_URL = "https://api.yelp.com/v3/businesses/search"

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

        # Rechercher des restaurants via l'API Yelp
        params = {
            "state": selected_department,
            "location": f"{selected_city}, France",     # Ville sélectionnée
            "term": "restaurants",            # Recherche de restaurants
            "limit": 10,                      # Nombre de résultats à récupérer
            "open_now": "True",               # Restaurants ouverts
            "sort_by": "distance",            # Tri par note (désactivé ici)
            "radius": 20000                   # distance en mètres
        }
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Accept": "application/json"
        }

        response = requests.get(YELP_URL, headers=headers, params=params)

        # Vérification de la réponse
        if response.status_code == 200:
            data = response.json()
            businesses = data.get("businesses", [])
            
            # Filtrage pour inclure uniquement les restaurants en France
            businesses_in_france = [
                business for business in businesses
                if business.get("location", {}).get("country") == "FR"
            ]
            
            if businesses_in_france:
                st.write(f"Restaurants trouvés à {selected_city}, {selected_department} (France):")
                for business in businesses_in_france:
                    name = business.get("name", "Nom indisponible")
                    address = ", ".join(business["location"].get("display_address", []))
                    rating = business.get("rating", "Non disponible")
                    review_count = business.get("review_count", "Non disponible")
                    image_url = business.get("image_url", "Non disponible")
                    phone = business.get("display_phone", "Non disponible")
                    lienG = lien_google(name, business["location"].get("city"))

                    st.write(f"- **{name}**")
                    if image_url:
                        st.image(f"{image_url}", width=150)
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
        else:
            st.write("Erreur lors de la récupération des données des restaurants.")
    else:
        st.write("Aucun département correspondant trouvé. Essayez une autre recherche.")
else:
    st.write("Veuillez entrer un nom ou un numéro de département pour commencer.")
