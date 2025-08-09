"""
Configuration module for AutoRender AI
"""

import os
import torch


class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Server settings
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # AI Model settings
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # YOLO settings
    YOLO_MODEL_PATH = "yolov8l-world.pt"
    YOLO_CONFIDENCE = 0.5
    
    # Stable Diffusion settings
    SD_MODEL_ID = "runwayml/stable-diffusion-v1-5"
    SD_TORCH_DTYPE = torch.float16 if torch.cuda.is_available() else torch.float32
    
    # Image processing settings
    MAX_IMAGE_SIZE = 1024
    SD_MAX_SIZE = 768  # Stable Diffusion works best with smaller images
    DEFAULT_EDGE_BLUR = 0
    
    # Caching settings
    LRU_CACHE_SIZE = 32
    SD_CACHE_SIZE = 16
    
    # Ngrok settings (for Colab)
    ENABLE_NGROK = os.environ.get('ENABLE_NGROK', 'False').lower() == 'true'
    NGROK_AUTH_TOKEN = os.environ.get('NGROK_AUTH_TOKEN')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


class ColabConfig(Config):
    """Colab-specific configuration"""
    DEBUG = True
    ENABLE_NGROK = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'colab': ColabConfig,
    'default': DevelopmentConfig
} 