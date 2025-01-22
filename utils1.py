import streamlit as st
import pandas as pd
import re

# Fonction pour enlever les accents sans unicodedata
def enlever_accents(chaine):
    if isinstance(chaine, str):
        accents = {
            'a': 'àáâäãå',
            'e': 'èéêë',
            'i': 'ìíîï',
            'o': 'òóôöõ',
            'u': 'ùúûü',
            'c': 'ç',
            'n': 'ñ',
            'A': 'ÀÁÂÄÃÅ',
            'E': 'ÈÉÊË',
            'I': 'ÌÍÎÏ',
            'O': 'ÒÓÔÖÕ',
            'U': 'ÙÚÛÜ',
            'C': 'Ç',
            'N': 'Ñ'
        }
        for char, accented_chars in accents.items():
            chaine = re.sub(f"[{accented_chars}]", char, chaine)
        return chaine
    return chaine