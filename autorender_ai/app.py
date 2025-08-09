"""
Flask application factory for AutoRender AI
"""

import os
from flask import Flask

from .config import config
from .routes import background_bp, detection_bp, health_bp
from .models.ai_models import model_manager


def create_app(config_name=None):
    """
    Application factory function.
    
    Args:
        config_name (str): Configuration to use ('development', 'production', 'colab')
        
    Returns:
        Flask: Configured Flask application
    """
    # Determine configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize models (lazy loading)
    with app.app_context():
        # You can pre-load models here if needed
        # model_manager.load_all_models()
        pass
    
    # Register blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(background_bp)
    app.register_blueprint(detection_bp)
    
    # Setup ngrok if enabled (for Colab)
    if app.config.get('ENABLE_NGROK'):
        try:
            from flask_ngrok import run_with_ngrok
            run_with_ngrok(app)
            print("🌐 Ngrok tunnel enabled")
        except ImportError:
            print("⚠️  flask-ngrok not available, running without tunnel")
    
    return app
