"""
AutoRender AI - Main Application Entrypoint

A Flask-based microservice for AI-powered image processing including:
- Background removal and replacement
- AI-generated background swapping using Stable Diffusion
- Object detection and smart cropping
- Face detection and cropping

Usage:
    python app.py                    # Run in development mode
    FLASK_ENV=production python app.py  # Run in production mode
    FLASK_ENV=colab python app.py    # Run in Colab mode with ngrok
"""

import os
from autorender_ai import create_app

# Create the Flask application
app = create_app()

if __name__ == "__main__":
    # Get configuration from environment or use defaults
    host = app.config.get('HOST', '0.0.0.0')
    port = app.config.get('PORT', 5000)
    debug = app.config.get('DEBUG', False)
    
    print(f"🚀 Starting AutoRender AI on {host}:{port}")
    print(f"📊 Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"🔧 Debug mode: {debug}")
    
    # Start the application
    if app.config.get('ENABLE_NGROK'):
        # Ngrok is already set up in create_app
        app.run()
    else:
        app.run(host=host, port=port, debug=debug)
