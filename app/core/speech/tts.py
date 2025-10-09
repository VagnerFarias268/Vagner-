"""Text-to-Speech using ElevenLabs"""
import os
from dotenv import load_dotenv
from pydub import AudioSegment

load_dotenv()

# Try both SDK styles (new vs old)
NEW_SDK = False
try:
    from elevenlabs.client import ElevenLabs  # new SDK
    from elevenlabs import VoiceSettings
    NEW_SDK = True
except ImportError:
    import elevenlabs  # old SDK
    from elevenlabs import VoiceSettings


def synthesize_to_file(text: str, phone: str, out_dir: str = "materials/temp") -> str:
    """
    Generate speech from text using ElevenLabs TTS and save as OGG.
    Output file: reply_<phone>.ogg
    """

    api_key = os.getenv("ELEVENLABS_API_KEY")
    voice_id = os.getenv("ELEVENLABS_VOICE_ID") or os.getenv("ELEVENLABS_VOICE_NAME")

    if not api_key:
        raise ValueError("❌ Missing ELEVENLABS_API_KEY in .env file")
    if not voice_id:
        raise ValueError("❌ Missing ELEVENLABS_VOICE_ID or ELEVENLABS_VOICE_NAME in .env file")

    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, f"reply_{phone}.ogg")
    tmp_mp3 = os.path.join(out_dir, f"temp_{phone}.mp3")

    if NEW_SDK:
        # New ElevenLabs client
        client = ElevenLabs(api_key=api_key)
        audio_bytes = client.generate(
            text=text,
            voice=voice_id,
            model="eleven_multilingual_v2",
            voice_settings=VoiceSettings(
                stability=0.5,
                similarity_boost=0.8,
                style=0.0,
                use_speaker_boost=True,
                speed=1.0,
            ),
            output_format="mp3_44100_128",
        )
    else:
        # Old SDK
        elevenlabs.set_api_key(api_key)
        audio_bytes = elevenlabs.generate(
            text=text,
            voice=voice_id,
            model="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )

    # Save MP3
    with open(tmp_mp3, "wb") as f:
        f.write(audio_bytes if isinstance(audio_bytes, (bytes, bytearray)) else b"".join(audio_bytes))

    # Convert MP3 → OGG (WhatsApp-compatible)
    audio = AudioSegment.from_file(tmp_mp3, format="mp3")
    audio.export(out_file, format="ogg")
    os.remove(tmp_mp3)

    print(f"✅ Audio saved to {out_file}")
    return out_file

