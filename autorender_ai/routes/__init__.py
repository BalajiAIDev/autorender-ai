"""
Routes module for AutoRender AI

Contains Flask blueprints for:
- Background processing endpoints
- Object detection endpoints
- Utility endpoints
"""

from .background_routes import background_bp
from .detection_routes import detection_bp
from .health_routes import health_bp

__all__ = ["background_bp", "detection_bp", "health_bp"]
