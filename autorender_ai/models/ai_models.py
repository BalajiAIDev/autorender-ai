"""
AI Models initialization and management
"""

import torch
from diffusers import StableDiffusionPipeline
from ultralytics import YOLO
import smartcrop

from ..config import Config


class ModelManager:
    """Manages AI model loading and initialization"""
    
    def __init__(self, config=None):
        self.config = config or Config()
        self.device = self.config.DEVICE
        
        # Initialize models
        self.yolo_model = None
        self.sd_pipe = None
        self.smart_crop = None
        
        print(f"Using device: {self.device}")
        
    def load_yolo_model(self):
        """Load YOLO model for object detection"""
        if self.yolo_model is None:
            print("Loading YOLO model...")
            try:
                self.yolo_model = YOLO(self.config.YOLO_MODEL_PATH)
                print("YOLO model loaded successfully.")
            except Exception as e:
                print(f"Failed to load YOLO model: {e}")
                raise
        return self.yolo_model
    
    def load_stable_diffusion_model(self):
        """Load Stable Diffusion model for background generation"""
        if self.sd_pipe is None:
            print("Loading Stable Diffusion model (this may take a while)...")
            try:
                self.sd_pipe = StableDiffusionPipeline.from_pretrained(
                    self.config.SD_MODEL_ID,
                    torch_dtype=self.config.SD_TORCH_DTYPE
                )
                self.sd_pipe = self.sd_pipe.to(self.device)
                print("Stable Diffusion model loaded successfully.")
            except Exception as e:
                print(f"Could not load Stable Diffusion model. /swap-background will not work. Error: {e}")
                self.sd_pipe = None
        return self.sd_pipe
    
    def load_smart_crop(self):
        """Load SmartCrop for intelligent image cropping"""
        if self.smart_crop is None:
            print("Initializing SmartCrop...")
            self.smart_crop = smartcrop.SmartCrop()
            print("SmartCrop initialized successfully.")
        return self.smart_crop
    
    def load_all_models(self):
        """Load all available models"""
        models = {}
        
        try:
            models['yolo'] = self.load_yolo_model()
        except Exception as e:
            print(f"YOLO model loading failed: {e}")
            models['yolo'] = None
            
        try:
            models['stable_diffusion'] = self.load_stable_diffusion_model()
        except Exception as e:
            print(f"Stable Diffusion model loading failed: {e}")
            models['stable_diffusion'] = None
            
        try:
            models['smart_crop'] = self.load_smart_crop()
        except Exception as e:
            print(f"SmartCrop loading failed: {e}")
            models['smart_crop'] = None
            
        return models
    
    def get_model_status(self):
        """Get the status of all models"""
        return {
            'yolo': self.yolo_model is not None,
            'stable_diffusion': self.sd_pipe is not None,
            'smart_crop': self.smart_crop is not None,
            'device': str(self.device)
        }


# Global model manager instance
model_manager = ModelManager() 