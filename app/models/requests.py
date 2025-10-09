"""Request models"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class WebhookMessage(BaseModel):
    """WhatsApp webhook message structure"""
    type: str
    from_: str = None
    id: str = None
    timestamp: str = None
    
    class Config:
        extra = "allow"  # Allow additional fields


class WebhookValue(BaseModel):
    """WhatsApp webhook value structure"""
    messaging_product: str
    metadata: Dict[str, Any]
    contacts: Optional[List[Dict[str, Any]]] = None
    messages: Optional[List[Dict[str, Any]]] = None
    
    class Config:
        extra = "allow"


class WebhookChange(BaseModel):
    """WhatsApp webhook change structure"""
    value: Dict[str, Any]
    field: str


class WebhookEntry(BaseModel):
    """WhatsApp webhook entry structure"""
    id: str
    changes: List[Dict[str, Any]]


class WebhookRequest(BaseModel):
    """WhatsApp webhook request structure"""
    object: str
    entry: List[Dict[str, Any]]

