"""Payment service for handling payment links"""
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class PaymentService:
    """Service for managing payment links and pricing"""
    
    def __init__(self):
        # Payment links from environment variables
        self.normal_link = os.getenv("PAYMENT_LINK_NORMAL", "https://pay.example.com/normal")
        self.discount_40_link = os.getenv("PAYMENT_LINK_DISCOUNT40", "https://pay.example.com/discount40")
        self.discount_50_link = os.getenv("PAYMENT_LINK_DISCOUNT50", "https://pay.example.com/discount50")
    
    def get_payment_link(self, price_objection: bool = False, max_discount: bool = False) -> str:
        """
        Get appropriate payment link based on customer situation
        
        Args:
            price_objection: Whether customer has price concerns
            max_discount: Whether to offer maximum discount (50% discount)
        
        Returns:
            Payment link URL
            - Normal: no discount
            - price_objection: 40% discount
            - price_objection + max_discount: 50% discount
        """
        if price_objection and max_discount:
            return self.discount_50_link
        elif price_objection:
            return self.discount_40_link
        else:
            return self.normal_link


# Singleton instance
_payment_service: Optional[PaymentService] = None


def get_payment_service() -> PaymentService:
    """Get payment service singleton"""
    global _payment_service
    if _payment_service is None:
        _payment_service = PaymentService()
    return _payment_service

