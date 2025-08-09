"""
Health and status routes
"""

from flask import Blueprint, jsonify

from ..models.ai_models import model_manager
from .. import __version__

# Create blueprint
health_bp = Blueprint('health', __name__)


@health_bp.route("/", methods=["GET"])
@health_bp.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint.
    """
    return jsonify({
        "status": "AutoRender AI API running",
        "version": __version__,
        "service": "autorender-ai"
    })


@health_bp.route("/status", methods=["GET"])
def status_endpoint():
    """
    Get detailed system status including model availability.
    """
    model_status = model_manager.get_model_status()
    
    return jsonify({
        "status": "running",
        "version": __version__,
        "models": model_status,
        "endpoints": {
            "background": ["/remove-bg", "/swap-background"],
            "detection": ["/detect", "/face-crop", "/smart-crop", "/detect-info"],
            "health": ["/", "/health", "/status"]
        }
    })


@health_bp.route("/models/load", methods=["POST"])
def load_models_endpoint():
    """
    Force load all models (useful for warming up).
    """
    try:
        models = model_manager.load_all_models()
        model_status = model_manager.get_model_status()
        
        return jsonify({
            "success": True,
            "message": "Models loaded",
            "models": model_status
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500 