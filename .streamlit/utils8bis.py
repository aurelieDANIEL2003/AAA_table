import os
import base64
import streamlit as st

def fond(side_bg):
    # Vérifier si le fichier existe
    if not os.path.exists(side_bg):
        st.error(f"❌ Le fichier {side_bg} n'existe pas. Vérifiez son chemin !")
        return

    # Lire l'image en base64
    with open(side_bg, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    # Détecter l'extension du fichier
    side_bg_ext = side_bg.split(".")[-1]

    # Appliquer le CSS à la sidebar
    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] > div:first-child {{
            background-image: url("data:image/{side_bg_ext};base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            height: 100vh;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Forcer Streamlit à rafraîchir le CSS
    st.write("")