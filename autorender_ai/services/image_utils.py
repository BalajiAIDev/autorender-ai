"""
Image processing utilities and helper functions
"""

import base64
import requests
from io import BytesIO
from PIL import Image
from flask import request


class ImageUtils:
    """Utility class for image processing operations"""
    
    @staticmethod
    def load_image_from_request():
        """
        Handles loading an image from either a file upload or a JSON URL.
        
        Returns:
            tuple: (PIL.Image, form_data_dict)
        
        Raises:
            ValueError: If no valid image source is provided
        """
        if request.content_type and request.content_type.startswith('application/json'):
            data = request.get_json()
            if not data or 'image_url' not in data:
                raise ValueError("Missing 'image_url' in JSON body")
            
            response = requests.get(data['image_url'])
            response.raise_for_status()  # Raises an exception for bad status codes
            return Image.open(BytesIO(response.content)).convert("RGB"), data
            
        elif 'image' in request.files:
            return Image.open(request.files['image']).convert("RGB"), request.form
        else:
            raise ValueError(
                "No image provided. Use 'image' in a multipart/form-data request "
                "or 'image_url' in a JSON request."
            )
    
    @staticmethod
    def image_to_base64(image, format="PNG"):
        """
        Converts a PIL Image to a base64 string.
        
        Args:
            image (PIL.Image): The image to convert
            format (str): Output format (PNG, JPEG, etc.)
            
        Returns:
            str: Base64 encoded image string
        """
        buffer = BytesIO()
        image.save(buffer, format=format)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    @staticmethod
    def compress_image(image, max_size=1024):
        """
        Compresses an image to a maximum dimension while maintaining aspect ratio.
        
        Args:
            image (PIL.Image): The image to compress
            max_size (int): Maximum dimension for width or height
            
        Returns:
            PIL.Image: Compressed image
        """
        if image.width > max_size or image.height > max_size:
            image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        return image
    
    @staticmethod
    def image_to_bytes(image, format='PNG'):
        """
        Converts a PIL Image to bytes for caching purposes.
        
        Args:
            image (PIL.Image): The image to convert
            format (str): Output format
            
        Returns:
            bytes: Image as bytes
        """
        buffer = BytesIO()
        image.save(buffer, format=format)
        return buffer.getvalue()
    
    @staticmethod
    def bytes_to_image(image_bytes):
        """
        Converts bytes back to PIL Image.
        
        Args:
            image_bytes (bytes): Image bytes
            
        Returns:
            PIL.Image: Reconstructed image
        """
        return Image.open(BytesIO(image_bytes))
    
    @staticmethod
    def validate_hex_color(color_hex):
        """
        Validates and processes hex color input.
        
        Args:
            color_hex (str): Hex color string
            
        Returns:
            tuple: RGB color tuple
            
        Raises:
            ValueError: If color format is invalid
        """
        if not color_hex:
            return None
            
        color_hex = color_hex.lstrip('#')
        if len(color_hex) != 6:
            raise ValueError("Invalid background color format. Use a 6-digit hex code.")
        
        try:
            return tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
        except ValueError:
            raise ValueError("Invalid hex color format. Use a 6-digit hex code.")
