"""
Background processing service for removal and replacement
"""

from functools import lru_cache
from io import BytesIO
from PIL import Image, ImageFilter
from rembg import remove

from .image_utils import ImageUtils
from ..models.ai_models import model_manager
from ..config import Config


class BackgroundService:
    """Service for background removal and replacement operations"""
    
    def __init__(self, config=None):
        self.config = config or Config()
    
    @lru_cache(maxsize=32)
    def _process_background_removal_cached(self, image_bytes, bg_color_hex, edge_blur_radius):
        """
        Cached function to remove background and refine edges.
        
        Args:
            image_bytes (bytes): Image data as bytes (for hashability)
            bg_color_hex (str): Background color in hex format
            edge_blur_radius (int): Blur radius for edge refinement
            
        Returns:
            PIL.Image: Processed image
        """
        image = Image.open(BytesIO(image_bytes)).convert("RGBA")
        
        # Remove background
        foreground = remove(image)
        
        # Edge Refinement
        if edge_blur_radius > 0:
            mask = foreground.getchannel('A')
            mask = mask.filter(ImageFilter.GaussianBlur(radius=edge_blur_radius))
            foreground.putalpha(mask)
        
        # Background Color Replacement
        if bg_color_hex:
            bg_color = ImageUtils.validate_hex_color(bg_color_hex)
            if bg_color:
                background = Image.new("RGB", foreground.size, bg_color)
                background.paste(foreground, mask=foreground.getchannel('A'))
                return background
        
        return foreground
    
    def remove_background(self, image, bg_color=None, edge_blur_radius=0):
        """
        Remove background from an image with optional color replacement.
        
        Args:
            image (PIL.Image): Input image
            bg_color (str): Optional background color (hex)
            edge_blur_radius (int): Optional edge blur radius
            
        Returns:
            PIL.Image: Processed image
        """
        # Convert image to bytes for caching
        image_bytes = ImageUtils.image_to_bytes(image)
        
        return self._process_background_removal_cached(
            image_bytes, bg_color, edge_blur_radius
        )
    
    @lru_cache(maxsize=16)
    def _process_background_swap_cached(self, image_bytes, prompt, width, height):
        """
        Cached function to swap background using Generative AI.
        
        Args:
            image_bytes (bytes): Image data as bytes
            prompt (str): Text prompt for background generation
            width (int): Target width
            height (int): Target height
            
        Returns:
            PIL.Image: Image with new background
        """
        # Get Stable Diffusion model
        sd_pipe = model_manager.load_stable_diffusion_model()
        if not sd_pipe:
            raise RuntimeError("Stable Diffusion model is not available.")
        
        # Step 1: Foreground Segmentation
        original_image = Image.open(BytesIO(image_bytes))
        subject = remove(original_image)
        
        # Step 2: Background Generation
        print(f"Generating background for prompt: '{prompt}'")
        generated_bg = sd_pipe(prompt, width=width, height=height).images[0]
        
        # Step 3: Compositing
        # Ensure background is the correct size
        generated_bg = generated_bg.resize(subject.size)
        # Paste the subject onto the generated background using its alpha channel as a mask
        generated_bg.paste(subject, (0, 0), subject)
        
        return generated_bg
    
    def swap_background(self, image, prompt, width=None, height=None):
        """
        Swap background using AI-generated content.
        
        Args:
            image (PIL.Image): Input image
            prompt (str): Text prompt for background generation
            width (int): Optional target width
            height (int): Optional target height
            
        Returns:
            PIL.Image: Image with AI-generated background
        """
        # Use image dimensions if not specified
        if width is None:
            width = image.width
        if height is None:
            height = image.height
            
        # Convert image to bytes for caching
        image_bytes = ImageUtils.image_to_bytes(image)
        
        return self._process_background_swap_cached(
            image_bytes, prompt, width, height
        )
