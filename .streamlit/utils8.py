# import base64
# import streamlit as st

# def fond(side_bg):

#     side_bg_ext = 'png'

#     # Lecture et encodage de l'image
#     with open(side_bg, "rb") as file:
#         base64_img = base64.b64encode(file.read()).decode()

#     # Ajout du CSS pour rendre l'image responsive
#     st.markdown(
#         f"""
#         <style>
#         [data-testid="stSidebar"] > div:first-child {{
#             background: url(data:image/{side_bg_ext};base64,{base64_img}) no-repeat center center;
#             background-size: cover;
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )
import base64
import streamlit as st
import os

def fond(side_bg):
    # Détecter l'extension de l'image automatiquement
    side_bg_ext = os.path.splitext(side_bg)[-1][1:]

    # Lecture et encodage de l'image
    with open(side_bg, "rb") as file:
        base64_img = base64.b64encode(file.read()).decode()

    # Ajout du CSS pour rendre l'image responsive dans la barre latérale
    st.markdown(
        f"""
        <style>
        [data-testid="stSidebarContent"] {{
            background-image: url("data:image/{side_bg_ext};base64,{base64_img}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center center;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
