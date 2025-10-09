"""Response models"""
from typing import Optional, Any
from pydantic import BaseModel


class StatusResponse(BaseModel):
    """Generic status response"""
    status: str
    message: Optional[str] = None
    data: Optional[Any] = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    services: dict


class WebhookResponse(BaseModel):
    """Webhook processing response"""
    status: str
    media_sent: Optional[int] = None
    message: Optional[str] = None

