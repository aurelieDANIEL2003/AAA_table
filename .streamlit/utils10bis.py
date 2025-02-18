import base64
import streamlit as st

def autoplay_audio(audio_file_path: str):
    with open(audio_file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        
        md = f"""
        <audio id="audio_player" controls autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        <br>
        <label for="volume">Volume:</label>
        <input type="range" id="volume" min="0" max="1" step="0.1" value="0.5" oninput="document.getElementById('audio_player').volume=this.value">
        """

        st.markdown(md, unsafe_allow_html=True)


