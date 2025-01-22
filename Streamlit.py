import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import random
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
import ast 
import base64
import re
import requests



# Fonction pour obtenir les données des restaurants via l'API Yelp
def obtenir_restaurants(ville, departement):
    # Remplacez par votre clé d'API Yelp
    api_key = "-rNtfI2lxUWH6YHZBqnAeYQ9rzpcAAn8dT-wshmTRxwON7ytBFNjVq8hbt527dD_G2XnF5BLApATmZmcTP0RwxLxqjc5MnBGfFY0Rb03fJ3Y9LJwvAn4fLIgAY5_Z3Yx"
    headers = {'Authorization': f'Bearer {api_key}'}
    url = f'https://api.yelp.com/v3/businesses/search?location={ville}%20{departement}&categories=restaurants'
    response = requests.get(url, headers=headers)
    data = response.json()
    
    # Extraction des informations pertinentes
    businesses = data.get('businesses', [])
    restaurants_data = [{
        'nom': business['name'],
        'note': business['rating'],
        'adresse': ", ".join(business['location']['address1']),
        'telephone': business['phone'],
        'prix': business.get('price', 'N/A')
    } for business in businesses]
    
    return pd.DataFrame(restaurants_data)

# Interface Streamlit
st.title('Application de Recherche de Restaurants')

# Saisie du département
departement_input = st.text_input('Entrez le département :', '')

# Saisie de la ville avec validation des 3 premières lettres
ville_input = st.text_input('Entrez les 3 premières lettres de la ville :', '')



# Vérification de la saisie de la ville (3 lettres minimum)
if ville_input and len(ville_input) >= 3 and re.match(r'^[a-zA-Z]{3}', ville_input):
    if departement_input:
        # Recherche des restaurants dans la ville et le département
        st.write(f'Recherche de restaurants à {ville_input} - {departement_input}...')
        df = obtenir_restaurants(ville_input, departement_input)
        if not df.empty:
            st.dataframe(df)
            restaurant_selectionne = st.selectbox('Choisissez un restaurant :', df['nom'])
            infos_restaurant = df[df['nom'] == restaurant_selectionne].iloc[0]
            st.write(f"### {restaurant_selectionne}")
            st.write(f"Note : {infos_restaurant['note']}")
            st.write(f"Prix : {infos_restaurant['prix']}")
            st.write(f"Adresse : {infos_restaurant['adresse']}")
            st.write(f"Téléphone : {infos_restaurant['telephone']}")
        else:
            st.write('Aucun restaurant trouvé pour cette ville et département.')
    else:
        st.write('Veuillez entrer un département.')
else:
    if ville_input:
        st.write('Veuillez entrer au moins 3 lettres pour la ville.')
