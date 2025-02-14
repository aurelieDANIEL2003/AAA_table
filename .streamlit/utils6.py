import folium
import requests
import json
import pandas as pd
import requests
from utils2 import lien_google
from utils7 import geocode

def carte (df_filtered, selected_city):

    # Créer un DataFrame à partir des données
    restaurants_data = []
    for _, row in df_filtered.iterrows():
        name = row['name']
        latitude = row['coordinates.latitude']
        longitude = row['coordinates.longitude']
        address = ", ".join(row.get("location.display_address", []))  
        url = row['url']
        lienG = lien_google(name, row["location.city"])
        restaurants_data.append({'Name': name, 'Latitude': latitude, 'Longitude': longitude, 'Address': address, 'URL':url, 'URL2':lienG})

    df_restaurants = pd.DataFrame(restaurants_data)

    # Initialiser la carte centrée sur Paris (vous pouvez ajuster selon votre besoin)
    map_center = geocode(selected_city)[::-1] # Coordonnées centrées sur la ville choisie
    m = folium.Map(location=map_center, zoom_start=13)
   
       
     # Ajouter des marqueurs pour chaque restaurant
    for idx, row in df_restaurants.iterrows():
        popup_content = f"""
        <b>{row['Name']}</b><br>
        {row['Address']}<br>
        <a href="{row['URL']}" target="_blank">Lien vers Yelp</a><br>
        <a href="{row['URL2']}" target="_blank">Lien vers Google</a>
        """
        folium.Marker(
            [row['Latitude'], row['Longitude']],
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(icon='cutlery', color='blue')
        ).add_to(m)

    return m

   ## Sauvegarder la carte sous forme de fichier HTML
    # m.save("restaurants_map.html")
    # print("Carte sauvegardée sous 'restaurants_map.html'.")
