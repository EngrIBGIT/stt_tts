import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OMEIFE_TTS_URL = "https://apis.omeife.ai/api/v1/user/translation/speech/query"
OMEIFE_STT_URL = "https://apis.omeife.ai/api/v1/user/speech-to-text"
OMEIFE_SRT_TRANSLATE_URL = "https://apis.omeife.ai/api/v1/user/developer/srt-translate"
OMEIFE_API_TOKEN = os.getenv("OMEIFE_API_TOKEN")


def text_to_speech_omeife(text: str, language: str, persona: str) -> str:
    """
    Converts text to speech using the Omeife TTS API.
    
    Args:
        text (str): The text to convert.
        language (str): Language to generate the speech (e.g., 'english', 'hausa', 'pidgin').
        persona (str): Voice persona (e.g., 'male', 'female', 'default').

    Returns:
        str: The local path to the generated audio file.
    """
    # Ensure headers are defined
    headers = {
        "Authorization": f"Bearer {OMEIFE_API_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    
    # Payload for the POST request
    payload = {
        "text": text,
        "language": language,
        "persona": persona,
    }

    try:
        # Send POST request to the Omeife TTS API
        response = requests.post(OMEIFE_TTS_URL, headers=headers, json=payload)
        
        # Handle errors and process response
        if response.status_code == 401:
            raise Exception("Unauthenticated: The API token may be invalid or expired.")
        elif response.status_code != 200:
            raise Exception(f"TTS Error: {response.json().get('message', 'Unknown error')}")

        # Retrieve the audio URL and download the file
        audio_url = response.json().get("audio_url")
        audio_file = f"{persona}_response.mp3"
        
        # Download the audio file
        audio_response = requests.get(audio_url)
        with open(audio_file, "wb") as file:
            file.write(audio_response.content)

        return audio_file
    except Exception as e:
        raise Exception(f"Error during TTS: {str(e)}")



def speech_to_text_omeife(audio_path: str, language: str) -> str:
    """
    Converts speech to text using the Omeife STT API.

    Args:
        audio_path (str): The path to the uploaded audio file.
        language (str): The language of the audio (e.g., 'english', 'hausa', 'pidgin').

    Returns:
        str: Transcription of the audio file.
    """
    headers = {
        "Authorization": f"Bearer {OMEIFE_API_TOKEN}",
        "Accept": "application/json",
    }
    files = {
        "file": open(audio_path, "rb"),
        "language": (None, language),
    }

    response = requests.post(OMEIFE_STT_URL, headers=headers, files=files)

    if response.status_code == 200:
        return response.json().get("text", "No transcription available.")
    else:
        raise Exception(f"STT Error: {response.json().get('message', 'Unknown error')}")


def translate_srt_file(srt_path: str, from_language: str, to_language: str) -> str:
    """
    Translates SRT subtitles from one language to another using Omeife API.

    Args:
        srt_path (str): The path to the SRT file.
        from_language (str): The source language (e.g., 'english').
        to_language (str): The target language (e.g., 'hausa', 'pidgin').

    Returns:
        str: The URL of the translated SRT file.
    """
    headers = {
        "Authorization": f"Bearer {OMEIFE_API_TOKEN}",
        "Accept": "application/json",
        "Content-Type": "multipart/form-data",
    }
    files = {
        "file": open(srt_path, "rb"),
        "from": (None, from_language),
        "to": (None, to_language),
    }

    response = requests.post(OMEIFE_SRT_TRANSLATE_URL, headers=headers, files=files)

    if response.status_code == 200:
        return response.json().get("file_path")
    else:
        raise Exception(f"SRT Translation Error: {response.json().get('message', 'Unknown error')}")
