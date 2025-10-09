"""Payment link service"""
from app.config import get_settings


class PaymentService:
    """Payment link management"""
    
    def __init__(self):
        settings = get_settings()
        self.links = {
            'normal': settings.PAYMENT_LINK_NORMAL,
            'discount40': settings.PAYMENT_LINK_DISCOUNT40,
            'discount50': settings.PAYMENT_LINK_DISCOUNT50
        }
    
    def get_payment_link(self, price_objection: bool = False, max_discount: bool = False) -> str:
        """Get appropriate payment link based on customer objections"""
        if price_objection and max_discount:
            return self.links['discount50']
        if price_objection:
            return self.links['discount40']
        return self.links['normal']


# Singleton instance
_payment_service = None


def get_payment_service() -> PaymentService:
    """Get payment service singleton"""
    global _payment_service
    if _payment_service is None:
        _payment_service = PaymentService()
    return _payment_service

