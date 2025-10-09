"""Text processing utilities"""
import re


def normalize_text(text: str) -> str:
    """Normalize whitespace in text"""
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def contains_keywords(text: str, keywords: list) -> bool:
    """Check if text contains any of the keywords (case-insensitive)"""
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in keywords)


def extract_phone_number(text: str) -> str:
    """Extract phone number from text"""
    # Brazilian phone number pattern
    pattern = r'\+?55\s?(\d{2})\s?(\d{4,5})-?(\d{4})'
    match = re.search(pattern, text)
    if match:
        return match.group(0)
    return ""

