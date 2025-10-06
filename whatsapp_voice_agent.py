import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from dotenv import load_dotenv
import logging
import json
import openai

from utils import download_audio_from_whatsapp, upload_audio_to_whatsapp, send_audio_to_user, audio_to_text, text_to_audio
 
# Load environment variables
load_dotenv()

app = FastAPI(title="WhatsApp Cloud API Webhook")

# Set up logging
logging.basicConfig(level=logging.INFO)

# Environment variables
VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "my_secret_token")
WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


@app.get("/webhook")
async def verify_webhook(request: Request):
    """
    Step 1: Meta verification endpoint.
    When you add your webhook in developers.facebook.com, Meta sends a GET request.
    """
    params = dict(request.query_params)
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    logging.info(f"Webhook verification attempt: {params}")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge or "")
    else:
        raise HTTPException(status_code=403, detail="Verification failed")


@app.post("/webhook")
async def receive_webhook(request: Request):
    """
    Step 2: Handle incoming WhatsApp messages via POST requests.
    """
    try:
        body = await request.json()
        logging.info(f"Incoming webhook: {json.dumps(body, indent=2)}")

        # Extract message if available
        entry = body.get("entry", [])
        if not entry:
            return JSONResponse({"status": "no entry"})

        changes = entry[0].get("changes", [])
        if not changes:
            return JSONResponse({"status": "no changes"})

        value = changes[0].get("value", {})
        messages = value.get("messages", [])

        if not messages:
            return JSONResponse({"status": "no messages"})

        message = messages[0]
        sender_id = message["from"]
        message_type = message["type"]

        logging.info(f"Message type: {message_type} from: {sender_id}")

        if message_type == "text":
            text = message["text"]["body"]
            logging.info(f"Text message: {text}")

            # Here you can trigger your GPT + ElevenLabs logic later
            return JSONResponse({
                "status": "text received",
                "from": sender_id,
                "message_type": "text",
                "text": text
            })

        elif message_type == "audio":
            audio_id = message["audio"]["id"]
            logging.info(f"Audio message received. Media ID: {audio_id}")
            
            # 1️⃣ Download the audio file
            audio_path = download_audio_from_whatsapp(audio_id)

            # 2️⃣ Transcribe with OpenAI Whisper
            transcription = audio_to_text(audio_path)
            print("📝 Texto reconhecido:", transcription)
            # transcription = transcribe_audio_with_openai(audio_path)
            # transcription = "Hello World"

            # # 3️⃣ Generate GPT reply
            # # reply_text = generate_gpt_reply(transcription)
            # reply_text = "generate_gpt_reply"
            # logging.info(f"GPT reply: {reply_text}")
            
            # 4️⃣ Synthesize GPT reply to voice
            # reply_audio_path = synthesize_with_elevenlabs(reply_text)
            reply_audio_path = text_to_audio(transcription, output_path="voz_brasileira.ogg")
            # reply_audio_path = "out.mp3"
            
             # 5️⃣ Send voice back to user
            media_id = upload_audio_to_whatsapp("reply_audio_path") 
            send_audio_to_user(sender_id, media_id)
            
            # 6️⃣ Cleanup
            os.remove(audio_path)
            os.remove(reply_audio_path)

            logging.info(f"Transcription from {sender_id}: {transcription}")

            return {
                "status": "audio transcribed",
                "from": sender_id,
                "text": transcription,
            }
            
            # return JSONResponse({
            #     "status": "audio transcribed",
            #     "from": sender_id,
            #     "message_type": "audio",
            #     "media_id": audio_id
            # })

        else:
            logging.warning(f"Unsupported message type: {message_type}")
            return JSONResponse({"status": "unsupported", "type": message_type})

    except Exception as e:
        logging.exception("Error processing webhook:")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/test")
async def test(request: Request):
    audio_url = synthesize_with_elevenlabs("Helllo world")
    logging.info(f"Transcription from {audio_url}")
    return JSONResponse({"status": "no entry"})
    # return {
    #     "url": audio_url
    # }