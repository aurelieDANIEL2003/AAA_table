import base64
import streamlit as st

def fond(image_path):
    """Convertit une image locale en base64 et applique un fond d'écran en CSS."""
    try:
        with open(image_path, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode()

        css_code = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """
        st.markdown(css_code, unsafe_allow_html=True)
    
    except FileNotFoundError:
        st.error(f"❌ L'image '{image_path}' est introuvable. Vérifiez le chemin.")
