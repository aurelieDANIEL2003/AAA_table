import requests

def geocode(adresse):
    url = f"https://api-adresse.data.gouv.fr/search/?q={adresse}"
    response = requests.get(url)
    data = response.json()
    coords = data['features'][0]['geometry']['coordinates']
    return coords

