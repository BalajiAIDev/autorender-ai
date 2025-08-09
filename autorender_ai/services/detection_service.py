"""
Object detection and cropping service
"""

import cv2
import numpy as np
from PIL import Image

from ..models.ai_models import model_manager
from ..config import Config


class DetectionService:
    """Service for object detection and image cropping operations"""
    
    def __init__(self, config=None):
        self.config = config or Config()
    
    def detect_and_crop(self, image, prompt):
        """
        Detect an object via a prompt and crop to it.
        
        Args:
            image (PIL.Image): Input image
            prompt (str): Object detection prompt
            
        Returns:
            PIL.Image: Cropped image containing the detected object
            
        Raises:
            ValueError: If no matching object is found
        """
        # Get YOLO model
        yolo_model = model_manager.load_yolo_model()
        if not yolo_model:
            raise RuntimeError("YOLO model is not available.")
        
        # Set detection classes and run prediction
        yolo_model.set_classes([prompt])
        results = yolo_model.predict(
            image, 
            conf=self.config.YOLO_CONFIDENCE, 
            verbose=False
        )
        
        # Extract bounding boxes
        boxes = results[0].boxes
        if not len(boxes):
            raise ValueError("No matching object found.")
        
        # Get the first detection's bounding box
        x0, y0, x1, y1 = map(int, boxes.xyxy[0].cpu().numpy())
        
        # Crop the image
        cropped = image.crop((x0, y0, x1, y1))
        
        return cropped
    
    def face_crop(self, image, padding=50):
        """
        Detect and crop faces using OpenCV.
        
        Args:
            image (PIL.Image): Input image
            padding (int): Padding around detected face
            
        Returns:
            PIL.Image: Cropped image containing the face
            
        Raises:
            ValueError: If no face is detected
        """
        # Convert PIL to OpenCV format
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        # Load face cascade classifier
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) == 0:
            raise ValueError("No face detected in the image.")
        
        # Get the first detected face
        x, y, w, h = faces[0]
        
        # Add padding
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(image.width - x, w + 2 * padding)
        h = min(image.height - y, h + 2 * padding)
        
        # Crop the image
        cropped = image.crop((x, y, x + w, y + h))
        
        return cropped
    
    def smart_crop(self, image, width, height):
        """
        Perform smart cropping using SmartCrop algorithm.
        
        Args:
            image (PIL.Image): Input image
            width (int): Target width
            height (int): Target height
            
        Returns:
            PIL.Image: Smart-cropped image
        """
        smart_crop = model_manager.load_smart_crop()
        if not smart_crop:
            raise RuntimeError("SmartCrop is not available.")
        
        # Perform smart crop analysis
        result = smart_crop.crop(image, width, height)
        
        # Extract crop coordinates
        crop_box = (
            result['top_crop']['x'],
            result['top_crop']['y'],
            result['top_crop']['x'] + result['top_crop']['width'],
            result['top_crop']['y'] + result['top_crop']['height']
        )
        
        # Crop and resize
        cropped = image.crop(crop_box)
        cropped = cropped.resize((width, height), Image.Resampling.LANCZOS)
        
        return cropped
    
    def get_detection_info(self, image, prompt):
        """
        Get detection information without cropping.
        
        Args:
            image (PIL.Image): Input image
            prompt (str): Object detection prompt
            
        Returns:
            dict: Detection information including bounding boxes and confidence scores
        """
        # Get YOLO model
        yolo_model = model_manager.load_yolo_model()
        if not yolo_model:
            raise RuntimeError("YOLO model is not available.")
        
        # Set detection classes and run prediction
        yolo_model.set_classes([prompt])
        results = yolo_model.predict(
            image, 
            conf=self.config.YOLO_CONFIDENCE, 
            verbose=False
        )
        
        # Extract detection information
        boxes = results[0].boxes
        detections = []
        
        for box in boxes:
            x0, y0, x1, y1 = map(int, box.xyxy[0].cpu().numpy())
            confidence = float(box.conf[0].cpu().numpy())
            
            detections.append({
                'bbox': [x0, y0, x1, y1],
                'confidence': confidence,
                'class': prompt
            })
        
        return {
            'detections': detections,
            'count': len(detections)
        } 