import streamlit as st
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os
import asyncio

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
        # Translate text
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        translated = loop.run_until_complete(translator.translate(text_to_translate, src=input_lang_code, dest=output_lang_code))
        translated_text = translated.text
        st.success(f"Translation: {translated_text}")

        # Generate speech for the translated text
        tts = gTTS(text=translated_text, lang=output_lang_code)
        tts.save("translated_audio.mp3")

        # Provide download link and playback
        st.audio("translated_audio.mp3", format="audio/mp3")

        # Clean up file
        os.remove("translated_audio.mp3")
    except Exception as e:
        st.error(f"Translation failed: {e}")

##st.caption("Powered by Google Translate & gTTS")
