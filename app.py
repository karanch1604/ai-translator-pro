import streamlit as st
from googletrans import Translator, LANGUAGES
from langdetect import detect
from gtts import gTTS
import speech_recognition as sr
import tempfile
import time

# ---------- CONFIG ----------
st.set_page_config(page_title="AI Translator Pro Max", page_icon="🌍", layout="wide")

translator = Translator()
recognizer = sr.Recognizer()

# ---------- STYLE ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}
.chat-bubble {
    padding: 12px;
    border-radius: 12px;
    margin: 8px 0;
    max-width: 80%;
}
.user {
    background-color: #1e293b;
    margin-left: auto;
}
.bot {
    background-color: #064e3b;
    margin-right: auto;
}
.stButton>button {
    background: linear-gradient(90deg, #6366f1, #22c55e);
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown("<h1 style='text-align:center;'>🌍 AI Translator Pro Max</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>Chat-style AI Translator with Voice</p>", unsafe_allow_html=True)

# ---------- LANGUAGES ----------
languages = {v.title(): k for k, v in LANGUAGES.items()}
lang_list = sorted(languages.keys())

col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("From", lang_list, index=lang_list.index("English"))
with col2:
    target_lang = st.selectbox("To", lang_list, index=lang_list.index("Hindi"))

# ---------- SESSION STATE ----------
if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------- INPUT ----------
input_text = st.text_input("Type message...")

colA, colB = st.columns(2)

# ---------- VOICE INPUT ----------
with colA:
    if st.button("🎤 Speak"):
        try:
            with sr.Microphone() as source:
                st.info("Listening...")
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                input_text = text
                st.success(f"You said: {text}")
        except Exception as e:
            st.error("Voice input failed")

# ---------- TRANSLATE ----------
with colB:
    if st.button("🚀 Send"):
        if input_text.strip() != "":
            try:
                translated = translator.translate(
                    input_text,
                    src=languages[source_lang],
                    dest=languages[target_lang]
                )

                # Save chat
                st.session_state.chat.append((input_text, translated.text))

                # TTS
                try:
                    tts = gTTS(text=translated.text, lang=languages[target_lang])
                    audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    tts.save(audio_file.name)
                    st.audio(audio_file.name)
                except:
                    pass

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Enter message")

# ---------- CHAT DISPLAY ----------
st.markdown("---")
for user_msg, bot_msg in st.session_state.chat[::-1]:
    st.markdown(f"<div class='chat-bubble user'>🧑 {user_msg}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-bubble bot'>🌐 {bot_msg}</div>", unsafe_allow_html=True)

# ---------- CLEAR CHAT ----------
if st.button("🗑 Clear Chat"):
    st.session_state.chat = []

# ---------- FOOTER ----------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>Pro Max Version 🚀</p>", unsafe_allow_html=True)
