from bs4 import BeautifulSoup
import requests
import pandas as pd


def lien_google(name, location):
    restaurant = name.replace(" ", "+")+ "+" + location.replace(" ", "+")
    url_restaurant = f"https://www.google.com/search?q={restaurant}"
    return url_restaurant