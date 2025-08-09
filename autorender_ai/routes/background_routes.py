"""
Background processing routes
"""

from flask import Blueprint, jsonify, request

from ..services.background_service import BackgroundService
from ..services.image_utils import ImageUtils

# Create blueprint
background_bp = Blueprint('background', __name__)

# Initialize service
bg_service = BackgroundService()


@background_bp.route("/remove-bg", methods=["POST"])
def remove_bg_endpoint():
    """
    Removes the background from an image.
    Params: image or image_url, bg_color (optional hex), edge_blur_radius (optional int).
    """
    try:
        image, form = ImageUtils.load_image_from_request()
        image = ImageUtils.compress_image(image)

        # Get parameters
        bg_color = form.get("bg_color")
        edge_blur_radius = int(form.get("edge_blur_radius", 0))

        # Process image
        final_image = bg_service.remove_background(
            image, 
            bg_color=bg_color, 
            edge_blur_radius=edge_blur_radius
        )

        return jsonify({
            "success": True,
            "image": ImageUtils.image_to_base64(final_image)
        })
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@background_bp.route("/swap-background", methods=["POST"])
def swap_background_endpoint():
    """
    Swaps the background of an image using a generative AI prompt.
    Params: image or image_url, prompt, width (optional), height (optional).
    """
    try:
        image, form = ImageUtils.load_image_from_request()
        image = ImageUtils.compress_image(image, max_size=768)  # SD works best with smaller images

        # Get parameters
        prompt = form.get('prompt')
        if not prompt:
            return jsonify({"error": "A 'prompt' is required."}), 400

        width = int(form.get('width', image.width))
        height = int(form.get('height', image.height))

        # Process image
        final_image = bg_service.swap_background(
            image,
            prompt=prompt,
            width=width,
            height=height
        )

        return jsonify({
            "success": True,
            "image": ImageUtils.image_to_base64(final_image, format="JPEG")
        })
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        print(f"Error in /swap-background: {e}")
        return jsonify({"error": str(e)}), 500
