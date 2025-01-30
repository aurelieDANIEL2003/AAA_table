import json
import requests
import pandas as pd

def api(ville):

    # Clé API
    API_KEY = "FnAs6986-medBbzafaCtjB4dG-FAFNulPGg9wH5EJFdp6XjEoY4Bvq8pqYfY4x_HmtezfrONesvmvlRkf9NFRumxA4vhTiPyAw9GS5JtMEA1xKlJ_W70uydnXgeSZ3Yx"

    # URL de base
    url = "https://api.yelp.com/v3/businesses/search"

    # Limiter la distance max selon Yelp API (40 000 mètres)
    #distance = min(int(distance), 40000)

    # Paramètres fixes
    params = {
        "location": f"{ville}, France", # Exemple : ville
        "term": "restaurants",  # Exemple : type d'entreprise
        "limit": 50,            # Nombre de résultats
        "sort_by": "distance",  # Critères de tri
        "locale": "fr_FR"       # affichage en francais
       
    }

    # En-têtes HTTP
    headers = {
        "Authorization": f"Bearer {API_KEY}",  # Clé API
        "Accept": "application/json"          # Format attendu
    }

        #Envoi de la requête GET
    r = requests.get(url, headers=headers, params=params)

    # #Vérification du statut de la requête

    data = json.loads(r.text)
    df = pd.json_normalize(data)
    #data.keys()
    df = pd.json_normalize(r.json(), record_path="businesses")
    

    return df