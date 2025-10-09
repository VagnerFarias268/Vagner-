"""Speech-to-Text using OpenAI Whisper"""
import os
from dotenv import load_dotenv

load_dotenv()

# --- Flexible OpenAI client import ---
try:
    # New SDK (openai>=1.0.0)
    from openai import OpenAI
    _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def _transcribe(path: str):
        with open(path, "rb") as f:
            return _client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="pt"
            )

except ImportError:
    # Fallback for legacy SDK (<1.0.0)
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")

    def _transcribe(path: str):
        with open(path, "rb") as f:
            return openai.Audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="pt"
            )


def transcribe_file(path: str) -> str:
    """Transcribe audio file into text (Portuguese)."""
    resp = _transcribe(path)

    # Defensive handling: resp can be dict or object
    if isinstance(resp, dict):
        return resp.get("text", "")
    return getattr(resp, "text", str(resp))

