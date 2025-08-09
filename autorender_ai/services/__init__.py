"""
Services module for AutoRender AI

Contains business logic for:
- Background removal and replacement
- Image processing utilities
- Object detection services
- Smart cropping functionality
"""

from .background_service import BackgroundService
from .detection_service import DetectionService
from .image_utils import ImageUtils

__all__ = ["BackgroundService", "DetectionService", "ImageUtils"]
