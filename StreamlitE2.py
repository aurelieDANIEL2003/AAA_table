import streamlit as st
import pandas as pd
import requests
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Charger le fichier CSV contenant les départements et villes
df_loc1 = pd.read_csv('df_loc.csv')

# Clé API Yelp
API_KEY = "-rNtfI2lxUWH6YHZBqnAeYQ9rzpcAAn8dT-wshmTRxwON7ytBFNjVq8hbt527dD_G2XnF5BLApATmZmcTP0RwxLxqjc5MnBGfFY0Rb03fJ3Y9LJwvAn4fLIgAY5_Z3Yx"

# URL de base pour l'API Yelp
YELP_URL = "https://api.yelp.com/v3/businesses/search"

# Titre de l'application
st.title("Recherche de département, ville et restaurants en France")

# Entrée pour rechercher un département par nom ou numéro
query = st.text_input("Entrez le nom ou le numéro du département :").lower()

# Filtrer les départements correspondant à la requête
filtered_departments = df_loc1[
    df_loc1["nom_departement"].str.lower().str.contains(query) | 
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
        "location": selected_city,  # Ville sélectionnée
        "term": "restaurants",      # Recherche de restaurants
        "limit": 10,                # Nombre de résultats à récupérer
        "sort_by": "rating",        # Trier par note
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    response = requests.get(YELP_URL, headers=headers, params=params)

    # Vérification de la réponse
    if response.status_code == 200:
        data = response.json()
        businesses = data.get("businesses", [])

        if businesses:
            st.write(f"Restaurants trouvés à {selected_city}, {selected_department} :")
            for business in businesses:
                name = business.get("name", "Nom indisponible")
                address = ", ".join(business["location"].get("display_address", []))
                rating = business.get("rating", "Non disponible")
                image_url = business.get("image_url", "Non disponible")
                phone = business.get("display_phone", "Non disponible")
                st.write(f"- **{name}**")
                st.image(f"{image_url}", width=150)
                st.write(f"  - Adresse : {address}")
                st.write(f"  - Note : {rating} ⭐")
                st.write(f"  - Téléphone : {phone}")
                st.write("---")
        else:
            st.write("Aucun restaurant trouvé pour cette ville.")
    else:
        st.write("Erreur lors de la récupération des données des restaurants.")
else:
    st.write("Aucun département correspondant trouvé. Essayez une autre recherche.")




