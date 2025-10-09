"""File handling utilities"""
import os
from typing import Optional


def ensure_dir(directory: str) -> None:
    """Ensure directory exists, create if not"""
    os.makedirs(directory, exist_ok=True)


def get_file_extension(filename: str) -> str:
    """Get file extension (lowercase, without dot)"""
    _, ext = os.path.splitext(filename)
    return ext.lower().lstrip('.')


def is_image(filename: str) -> bool:
    """Check if file is an image"""
    image_extensions = {'jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp'}
    return get_file_extension(filename) in image_extensions


def is_video(filename: str) -> bool:
    """Check if file is a video"""
    video_extensions = {'mp4', 'avi', 'mov', 'mkv', 'webm'}
    return get_file_extension(filename) in video_extensions


def is_audio(filename: str) -> bool:
    """Check if file is audio"""
    audio_extensions = {'mp3', 'ogg', 'wav', 'm4a', 'aac'}
    return get_file_extension(filename) in audio_extensions


def get_safe_filename(filename: str) -> str:
    """Get safe filename by removing dangerous characters"""
    # Remove path separators and other dangerous characters
    safe = re.sub(r'[^\w\s\-\.]', '', filename)
    return safe.strip()


import re

