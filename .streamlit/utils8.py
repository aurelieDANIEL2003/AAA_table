import base64
import streamlit as st

def fond(side_bg):

    side_bg_ext = 'png'

    # Lecture et encodage de l'image
    with open(side_bg, "rb") as file:
        base64_img = base64.b64encode(file.read()).decode()

    # Ajout du CSS pour rendre l'image responsive
    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] > div:first-child {{
            background: url(data:image/{side_bg_ext};base64,{base64_img}) no-repeat center center;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )