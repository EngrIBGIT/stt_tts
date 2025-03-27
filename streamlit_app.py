import streamlit as st
from tts_stt_backend import text_to_speech_omeife, speech_to_text_omeife, translate_srt_file
from docx import Document
from fpdf import FPDF

# Set Streamlit page configuration
st.set_page_config(page_title="Speech Translator", page_icon="🤖", layout="centered")

# Styling
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(120deg, #87ceeb, #d8ffd6, #d3d3d3); /* Sky-blue, Lemon, Grey */
            font-family: Arial, sans-serif;
        }
        .stTitle {
            text-align: center;
        }
        .stHeader, h1, h2, h3, h4 {
            text-align: center;
            color: #333;
        }
        .stButton > button {
            background-color: #4682b4; /* Steel blue */
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Logo and Title
st.image("logo.jpeg", width=200)  # Add your centralized logo
st.title("Speech Translator 🤖")
st.subheader("Seamlessly Translate, Transcribe, and Speak Across Languages!")

# Text-to-Speech Section
st.header("🌍 Text-to-Speech")
text = st.text_area("Enter text to convert to speech:")
language = st.selectbox("Select Language:", ["english", "hausa", "pidgin"])
persona = st.selectbox("Select Voice Persona:", ["male", "female", "default"])

if st.button("Generate Speech"):
    try:
        audio_file = text_to_speech_omeife(text, language, persona)
        st.audio(audio_file, format="audio/mp3")
        st.download_button("Download Audio", open(audio_file, "rb"), file_name=audio_file)
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Speech-to-Text Section
st.header("🎙 Speech-to-Text")
uploaded_audio = st.file_uploader("Upload Audio File for Transcription (MP3 or WAV):", type=["mp3", "wav"])
stt_language = st.selectbox("Select Audio Language:", ["english", "hausa", "pidgin"])

if st.button("Transcribe Audio"):
    if not uploaded_audio:
        st.error("Please upload an audio file.")
    else:
        try:
            # Save uploaded file locally
            audio_path = f"temp_{uploaded_audio.name}"
            with open(audio_path, "wb") as f:
                f.write(uploaded_audio.getbuffer())

            transcription = speech_to_text_omeife(audio_path, stt_language)
            st.write("### Transcription:")
            st.text(transcription)

            # Generate Downloadable Outputs
            doc_file = "transcription.docx"
            pdf_file = "transcription.pdf"

            # Save as Word
            doc = Document()
            doc.add_paragraph(transcription)
            doc.save(doc_file)

            # Save as PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, transcription)
            pdf.output(pdf_file)

            st.download_button("Download as Word", open(doc_file, "rb"), file_name=doc_file)
            st.download_button("Download as PDF", open(pdf_file, "rb"), file_name=pdf_file)
        except Exception as e:
            st.error(f"Error: {str(e)}")

# SRT Translation Section
st.header("📄 Translate SRT Subtitles")
uploaded_srt = st.file_uploader("Upload SRT File for Translation:", type=["srt"])
source_language = st.selectbox("Source Language:", ["english"])
target_language = st.selectbox("Target Language:", ["hausa", "pidgin", "english"])

if st.button("Translate Subtitles"):
    try:
        if uploaded_srt:
            translated_srt_url = translate_srt_file(uploaded_srt.name, source_language, target_language)
            st.write("### Translated SRT File:")
            st.markdown(f"[Download Translated File]({translated_srt_url})")
        else:
            st.error("Please upload an SRT file.")
    except Exception as e:
        st.error(f"Error: {str(e)}")
