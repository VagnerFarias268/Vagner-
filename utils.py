import os
import requests
import tempfile
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
# import openai 
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
from pydub import AudioSegment
from openai import OpenAI
import whisper

load_dotenv()
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="WhatsApp Audio to Text Webhook")

# WhatsApp
VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")
WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = "YOUR_PHONE_NUMBER_ID"  # from Meta Dashboard

# # OpenAI
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# openai.api_key = OPENAI_API_KEY

# ElevenLabs
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
ELEVEN_VOICE_ID = os.getenv("ELEVEN_VOICE_ID")  # Your ElevenLabs voice ID

def upload_audio_to_whatsapp(file_path: str) -> str:
    """Uploads an audio file and returns media_id"""
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/media"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}"
    }

    files = {
        "file": open(file_path, "rb"),
        "type": (None, "audio/ogg")  # or "audio/mpeg" for mp3
    }

    res = requests.post(url, headers=headers, files=files)
    if res.status_code != 200:
        raise Exception(f"Upload failed: {res.text}")

    media_id = res.json().get("id")
    print(f"✅ Uploaded to WhatsApp. Media ID: {media_id}")
    return media_id

def send_audio_to_user(to_number: str, media_id: str):
    """Sends the uploaded audio back to the WhatsApp user."""
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "audio",
        "audio": {"id": media_id}
    }

    res = requests.post(url, headers=headers, json=data)
    if res.status_code != 200:
        raise Exception(f"Send failed: {res.text}")

    print(f"🎤 Audio sent to {to_number}")


def download_audio_from_whatsapp(media_id: str) -> str:
    """Download audio file from WhatsApp Cloud API."""
    # 1. Get the media URL
    url = f"https://graph.facebook.com/v17.0/{media_id}"
    headers = {"Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}"}
    res = requests.get(url, headers=headers, timeout=30)
    if res.status_code != 200:
        raise RuntimeError(f"Failed to get media URL: {res.text}")

    media_url = res.json().get("url")
    if not media_url:
        raise RuntimeError("Media URL not found in response")

    # 2. Download the actual media file
    res = requests.get(media_url, headers=headers, timeout=60)
    if res.status_code != 200:
        raise RuntimeError(f"Failed to download media: {res.text}")

    # Save to temporary file
    fd, temp_path = tempfile.mkstemp(suffix=".ogg")
    with os.fdopen(fd, "wb") as f:
        f.write(res.content)

    logging.info(f"Audio saved to: {temp_path}")
    return temp_path

# whisper
# def transcribe_audio_with_openai(file_path: str) -> str:
#     """Send the audio to OpenAI Whisper and get text."""
#     with open(file_path, "rb") as audio_file:
#         result = openai.Audio.transcriptions.create(
#             model="gpt-4o-mini-transcribe",  # Whisper equivalent
#             file=audio_file
#         )
#     return result.text

# def synthesize_with_elevenlabs(text: str) -> str:
#     """Convert text to speech using ElevenLabs TTS."""
#     url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_VOICE_ID}"
#     headers = {
#         "xi-api-key": ELEVEN_API_KEY,
#         "Content-Type": "application/json"
#     }
#     data = {"text": text}
#     r = requests.post(url, headers=headers, json=data, timeout=60)
#     if r.status_code not in (200, 201):
#         raise RuntimeError(f"ElevenLabs TTS failed: {r.text}")

#     fd, temp_path = tempfile.mkstemp(suffix=".mp3")
#     with os.fdopen(fd, "wb") as f:
#         f.write(r.content)
#     logging.info(f"Audio synthesized to: {temp_path}")
#     return temp_path

# ---------------------------
# STT Function (Audio → Text)
# ---------------------------
def audio_to_text(audio_path: str, language: str = "pt"):
    """
    Try Whisper API first; if quota fails, fall back to local Whisper.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        client = OpenAI(api_key=api_key)
        try:
            with open(audio_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language
                )
            text = transcript.text
            print(f"✅ Transcription (API): {text}")
            return text
        except Exception as e:
            print(f"⚠️ Whisper API failed: {e}")
            print("👉 Falling back to local Whisper...")

    # Local Whisper fallback
    model = whisper.load_model("small")  # or "base", "medium", "large"
    result = model.transcribe(audio_path, language=language)
    text = result["text"]
    print(f"✅ Transcription (Local): {text}")
    return text

# ---------------------------
# TTS Function (Text → Audio)
# ---------------------------
def text_to_audio(text: str, output_path: str = "out.ogg"):
    load_dotenv()
    api_key = os.getenv("ELEVENLABS_API_KEY")
    voice_id = os.getenv("ELEVENLABS_VOICE_ID")

    if not api_key:
        raise ValueError("❌ Missing ELEVENLABS_API_KEY in .env file")
    if not voice_id:
        raise ValueError("❌ Missing ELEVENLABS_VOICE_ID in .env file")

    client = ElevenLabs(api_key=api_key)

    # Generate MP3 from ElevenLabs
    response = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id="eleven_turbo_v2_5",
        output_format="mp3_44100_128",
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.8,
            style=0.0,
            use_speaker_boost=True,
            speed=1.0,
        ),
    )

    tmp_mp3 = "temp_audio.mp3"
    with open(tmp_mp3, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    # Convert to OGG
    audio = AudioSegment.from_file(tmp_mp3, format="mp3")
    audio.export(output_path, format="ogg")
    os.remove(tmp_mp3)

    print(f"✅ Audio saved to {output_path}")
    
    return output_path
