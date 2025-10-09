"""WhatsApp webhook endpoints"""
from fastapi import APIRouter, Request, HTTPException, Query, File, Form, UploadFile
from typing import Optional

from app.models.responses import WebhookResponse
from app.services.message_handler import get_message_handler
from app.config import get_settings
from app.core.ai.llm import generate_ai_response

router = APIRouter()


@router.get("/webhook")
async def webhook_verification(
    hub_mode: Optional[str] = Query(None, alias="hub.mode"),
    hub_challenge: Optional[str] = Query(None, alias="hub.challenge"),
    hub_verify_token: Optional[str] = Query(None, alias="hub.verify_token")
):
    """
    WhatsApp webhook verification endpoint
    This is called by Meta to verify the webhook URL
    """
    settings = get_settings()
    
    if hub_mode == "subscribe":
        # Verify the token matches
        if settings.WHATSAPP_VERIFY_TOKEN and hub_verify_token == settings.WHATSAPP_VERIFY_TOKEN:
            return int(hub_challenge)
        elif not settings.WHATSAPP_VERIFY_TOKEN:
            # If no verify token is set, accept any request (dev mode)
            return int(hub_challenge) if hub_challenge else 200
        else:
            raise HTTPException(status_code=403, detail="Verification token mismatch")
    
    raise HTTPException(status_code=400, detail="Invalid verification request")


@router.post("/webhook", response_model=WebhookResponse)
async def webhook_handler(request: Request):
    """
    WhatsApp webhook message handler
    Processes incoming messages from WhatsApp
    """
    data = await request.json()
    
    try:
        # Extract message data
        entry = data['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        
        # Check if there are messages
        if 'messages' not in value or not value['messages']:
            return WebhookResponse(status='no_messages')
        
        message = value['messages'][0]
        phone = message['from']
        
        # Process the message
        handler = get_message_handler()
        result = handler.process_message(phone, message)
        
        return WebhookResponse(
            status=result.get('status', 'ok'),
            media_sent=result.get('media_sent'),
            message=result.get('message')
        )
        
    except KeyError as e:
        print(f"Webhook payload error: {e}")
        raise HTTPException(status_code=400, detail=f'Invalid webhook payload: missing {e}')
    except Exception as e:
        print(f"Webhook processing error: {e}")
        raise HTTPException(status_code=500, detail=f'Internal error: {str(e)}')


# test endpoint for text or audio input

@router.post("/test")
async def test(
    text: Optional[str] = Form(None),
    audio: Optional[UploadFile] = File(None)
):
    """
    Test endpoint that accepts either text or audio via form-data
    
    Parameters:
    - text: Optional text input
    - audio: Optional audio file upload
    """
    if not text and not audio:
        raise HTTPException(status_code=400, detail="Either 'text' or 'audio' must be provided")
    
    result = {}
    
    # Handle text input
    if text:
        print(f"Received text: {text}")
        result["input_type"] = "text"
        result["text"] = text

        data = generate_ai_response(text)
        print(data)
        
        # Process text with message handler if needed
        # processed = handler.process_message("test_user", {"text": text})
        # result["response"] = processed
    
    # Handle audio input
    if audio:
        print(f"Received audio file: {audio.filename}, content_type: {audio.content_type}")
        
        # Read audio content
        audio_content = await audio.read()
        audio_size = len(audio_content)
        
        print(f"Audio file size: {audio_size} bytes")
        
        result["input_type"] = "audio"
        result["filename"] = audio.filename
        result["content_type"] = audio.content_type
        result["size_bytes"] = audio_size
        
        # Process audio with message handler if needed
        # handler = get_message_handler()
        # processed = handler.process_audio("test_user", audio_content)
        # result["response"] = processed
    
    return {
        "status": "ok",
        "data": result
    }
