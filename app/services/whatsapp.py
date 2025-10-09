"""WhatsApp Cloud API client"""
import os
import requests
from typing import Optional
from app.config import get_settings


class WhatsAppClient:
    """WhatsApp Cloud API integration"""
    
    def __init__(self):
        settings = get_settings()
        self.token = settings.WHATSAPP_ACCESS_TOKEN
        self.phone_id = settings.WHATSAPP_PHONE_ID
        self.base_url = 'https://graph.facebook.com/v20.0'
        self.temp_folder = settings.TEMP_FOLDER
        os.makedirs(self.temp_folder, exist_ok=True)
    
    def send_text(self, to: str, body: str) -> dict:
        """Send text message"""
        url = f"{self.base_url}/{self.phone_id}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            'type': 'text',
            'text': {'body': body}
        }
        headers = {'Authorization': f'Bearer {self.token}'}
        r = requests.post(url, json=payload, headers=headers)
        print('send_text', r.status_code, r.text)
        return r.json()
    
    def upload_media(self, file_path: str) -> dict:
        """Upload media file to WhatsApp"""
        url = f"{self.base_url}/{self.phone_id}/media"
        files = {'file': open(file_path, 'rb')}
        params = {'messaging_product': 'whatsapp'}
        headers = {'Authorization': f'Bearer {self.token}'}
        r = requests.post(url, files=files, data=params, headers=headers)
        print('upload_media', r.status_code, r.text)
        return r.json()
    
    def send_media(self, to: str, file_path: str) -> Optional[dict]:
        """Send media (image/video) message"""
        up = self.upload_media(file_path)
        media_id = up.get('id')
        if not media_id:
            print('upload failed', up)
            return None
        
        ext = file_path.split('.')[-1].lower()
        msg_type = 'image' if ext in ['jpg', 'jpeg', 'png'] else 'video'
        url = f"{self.base_url}/{self.phone_id}/messages"
        payload = {
            'messaging_product': 'whatsapp',
            'to': to,
            'type': msg_type,
            msg_type: {'id': media_id}
        }
        headers = {'Authorization': f'Bearer {self.token}'}
        r = requests.post(url, json=payload, headers=headers)
        print('send_media', r.status_code, r.text)
        return r.json()
    
    def send_audio(self, to: str, file_path: str) -> Optional[dict]:
        """Send audio message"""
        up = self.upload_media(file_path)
        media_id = up.get('id')
        if not media_id:
            print('upload failed', up)
            return None
        
        url = f"{self.base_url}/{self.phone_id}/messages"
        payload = {
            'messaging_product': 'whatsapp',
            'to': to,
            'type': 'audio',
            'audio': {'id': media_id}
        }
        headers = {'Authorization': f'Bearer {self.token}'}
        r = requests.post(url, json=payload, headers=headers)
        print('send_audio', r.status_code, r.text)
        
        # Delete temp file after sending
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"🗑️ Deleted temp audio file: {file_path}")
        except Exception as e:
            print("⚠️ Failed to delete temp audio file:", e)
        
        return r.json()
    
    def download_media_file(self, media_id: str, out_path: Optional[str] = None) -> str:
        """Download media file from WhatsApp"""
        out_path = out_path or os.path.join(self.temp_folder, media_id)
        url_meta = f"https://graph.facebook.com/v20.0/{media_id}"
        headers = {'Authorization': f'Bearer {self.token}'}
        r = requests.get(url_meta, headers=headers)
        meta = r.json()
        media_url = meta.get('url')
        if not media_url:
            raise ValueError('no media url')
        r2 = requests.get(media_url, headers=headers)
        with open(out_path, 'wb') as f:
            f.write(r2.content)
        return out_path


# Singleton instance
_whatsapp_client = None


def get_whatsapp_client() -> WhatsAppClient:
    """Get WhatsApp client singleton"""
    global _whatsapp_client
    if _whatsapp_client is None:
        _whatsapp_client = WhatsAppClient()
    return _whatsapp_client

