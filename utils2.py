from bs4 import BeautifulSoup
import requests
import pandas as pd


def lien_google(name, location):
    restaurant = name.replace(" ", "+")+ "+" + location.replace(" ", "+")
    url_restaurant = f"https://www.google.com/search?q={restaurant}"

    # si on veut rajouter des choses

    # html = requests.get(url_restaurant)
    # soup = BeautifulSoup(html.text, 'html.parser')

    #    # identification comme navigateur
    # navigator = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'
    # html = requests.get(url_restaurant, headers={'User-Agent': navigator})

    #     # Nous filtrons maintenant uniquement sur avis google sur la page :
    # soup_director = soup.find_all('span', {"class" : "Aq14fc"})
    # # # Puis nous cherchons tous les liens contenus dans cet encadré :
    # # links = soup_director.find_all('')


    return url_restaurant

