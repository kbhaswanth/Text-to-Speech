import streamlit as st
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os

# Streamlit app configuration
st.title("Language Translator & Text-to-Speech")

# Language selection
input_lang = st.selectbox("Select Input Language", options=list(LANGUAGES.values()))
output_lang = st.selectbox("Select Output Language", options=list(LANGUAGES.values()))

# Text input
text_to_translate = st.text_area("Enter text")

# Initialize translator
translator = Translator()

if st.button("Translate"):
    # Get language codes
    input_lang_code = [k for k, v in LANGUAGES.items() if v == input_lang][0]
    output_lang_code = [k for k, v in LANGUAGES.items() if v == output_lang][0]

    try:
        # Translate text (No asyncio needed)
        translated = translator.translate(text_to_translate, src=input_lang_code, dest=output_lang_code)
        translated_text = translated.text
        st.success(f"Translation: {translated_text}")

        # Generate speech for the translated text
        tts = gTTS(text=translated_text, lang=output_lang_code)
        audio_file = "translated_audio.mp3"
        tts.save(audio_file)

        # Provide download link and playback
        st.audio(audio_file, format="audio/mp3")

        # Clean up file (optional, but better to do this outside Streamlit's execution cycle)
        os.remove(audio_file)
    except Exception as e:
        st.error(f"Translation failed: {e}")

st.caption("Powered by Google Translate & gTTS")
