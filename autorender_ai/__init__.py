"""
AutoRender AI - Image Processing and AI-powered Background Manipulation

A Flask-based microservice that provides:
- Background removal and replacement
- AI-powered background generation using Stable Diffusion
- Object detection and cropping
- Smart image processing utilities
"""

__version__ = "1.0.0"
__author__ = "AutoRender Team"

# Import main application factory
from .app import create_app

__all__ = ["create_app"]
