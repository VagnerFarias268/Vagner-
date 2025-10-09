"""Message handling orchestration"""
import os
import random
from typing import Optional, Tuple

from app.config import get_settings
from app.core.ai.llm import generate_ai_response
from app.core.speech.stt import transcribe_file
from app.core.speech.tts import synthesize_to_file
from app.core.kb.manager import add_chat_to_kb
from app.core.kb.retriever import get_retriever
from app.services.whatsapp import get_whatsapp_client
from app.services.payment import get_payment_service


class MessageHandler:
    """Orchestrates message processing logic"""
    
    def __init__(self):
        self.settings = get_settings()
        self.whatsapp = get_whatsapp_client()
        self.payment = get_payment_service()
        self.retriever = get_retriever()
    
    def extract_user_text(self, message: dict) -> Tuple[Optional[str], Optional[str]]:
        """
        Extract text from message (text or audio)
        Returns: (user_text, error_message)
        """
        msg_type = message.get('type')
        
        if msg_type == 'text':
            return message['text']['body'], None
        
        elif msg_type == 'audio':
            try:
                media_id = message['audio']['id']
                path = self.whatsapp.download_media_file(
                    media_id,
                    out_path=os.path.join(self.settings.TEMP_FOLDER, 'input.ogg')
                )
                user_text = transcribe_file(path)
                return user_text, None
            except Exception as e:
                print("Audio transcription error:", e)
                return None, "Desculpe, não consegui processar o áudio."
        
        return None, None
    
    def get_relevant_media(self, user_text: str) -> list:
        """Get relevant media files from KB"""
        docs = self.retriever.get_relevant_documents(user_text)
        media_files = [
            d.metadata.get('file_path')
            for d in docs
            if d.metadata.get('type') == 'media' and d.metadata.get('file_path')
        ]
        return media_files
    
    def send_reply(self, phone: str, ai_reply: str):
        """Send text and audio reply"""
        # Send text
        self.whatsapp.send_text(phone, ai_reply)
        
        # Send TTS audio
        try:
            audio_path = synthesize_to_file(
                ai_reply,
                phone=phone,
                out_dir=self.settings.TEMP_FOLDER
            )
            self.whatsapp.send_audio(phone, audio_path)
        except Exception as e:
            print('TTS/send audio error:', e)
    
    def send_media_files(self, phone: str, media_files: list) -> int:
        """Send relevant media files"""
        sent = 0
        for mf in media_files:
            if mf and os.path.exists(mf):
                try:
                    self.whatsapp.send_media(phone, mf)
                    sent += 1
                except Exception as e:
                    print('send_media error', e)
        
        # 30% chance to send fallback media if nothing sent
        if sent == 0 and random.random() < 0.3:
            fallback = os.path.join(self.settings.MEDIA_FOLDER, 'before_after.jpg')
            if os.path.exists(fallback):
                try:
                    self.whatsapp.send_media(phone, fallback)
                    sent += 1
                except Exception as e:
                    print('fallback media error', e)
        
        return sent
    
    def detect_buying_intent(self, user_text: str, phone: str) -> bool:
        """Detect if user wants to buy and send payment link"""
        buying_keywords = [
            'quero comprar', 'vou comprar', 'fechar pedido',
            'me manda o link', 'link de pagamento', 'como pagar', 'onde pago'
        ]
        
        if any(kw in user_text.lower() for kw in buying_keywords):
            link = self.payment.get_payment_link(price_objection=False)
            self.whatsapp.send_text(
                phone,
                f'Perfeito! Aqui está o link para finalizar sua compra: {link}'
            )
            return True
        return False
    
    def handle_price_objection(self, user_text: str, phone: str) -> bool:
        """Handle price objections with discounted links"""
        price_keywords = ['caro', 'preço', 'muito caro']
        
        if any(kw in user_text.lower() for kw in price_keywords):
            link = self.payment.get_payment_link(price_objection=True, max_discount=False)
            self.whatsapp.send_text(
                phone,
                f'Entendo que o preço é uma preocupação. Posso te oferecer essa condição especial: {link}'
            )
            return True
        return False
    
    def process_message(self, phone: str, message: dict) -> dict:
        """
        Main message processing pipeline
        Returns: status dict
        """
        # Extract user text
        user_text, error = self.extract_user_text(message)
        
        if error:
            self.whatsapp.send_text(phone, error)
            return {'status': 'error', 'message': error}
        
        if not user_text:
            self.whatsapp.send_text(phone, 'Desculpe, não entendi. Pode repetir, por favor?')
            return {'status': 'no_input'}
        
        # Get relevant media from KB
        media_files = self.get_relevant_media(user_text)
        
        # Generate AI response
        ai_reply = generate_ai_response(user_text)
        
        # Archive conversation
        try:
            add_chat_to_kb(user_text, ai_reply, phone)
        except Exception as e:
            print('Warning: failed to archive chat:', e)
        
        # Send reply (text + audio)
        self.send_reply(phone, ai_reply)
        
        # Send relevant media
        sent_media = self.send_media_files(phone, media_files)
        
        # Check for buying intent
        if self.detect_buying_intent(user_text, phone):
            return {'status': 'buying_intent', 'media_sent': sent_media}
        
        # Handle price objection
        self.handle_price_objection(user_text, phone)
        
        return {'status': 'ok', 'media_sent': sent_media}


# Singleton instance
_message_handler = None


def get_message_handler() -> MessageHandler:
    """Get message handler singleton"""
    global _message_handler
    if _message_handler is None:
        _message_handler = MessageHandler()
    return _message_handler

