import streamlit as st

def fond(image_path):
    """Applique une image de fond en CSS via un conteneur HTML Streamlit."""
    css_code = f"""
    <style>
    .stApp {{
        background: url("{image_path}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)
