"""
Object detection and cropping routes
"""

from flask import Blueprint, jsonify, request

from ..services.detection_service import DetectionService
from ..services.image_utils import ImageUtils

# Create blueprint
detection_bp = Blueprint('detection', __name__)

# Initialize service
detection_service = DetectionService()


@detection_bp.route("/detect", methods=["POST"])
def detect_endpoint():
    """
    Detects an object via a prompt and crops to it.
    Params: image or image_url, prompt
    """
    try:
        image, form = ImageUtils.load_image_from_request()
        prompt = form.get('prompt')
        
        if not prompt:
            return jsonify({"error": "Prompt is required."}), 400

        # Detect and crop object
        cropped = detection_service.detect_and_crop(image, prompt)

        return jsonify({
            "success": True,
            "image": ImageUtils.image_to_base64(cropped)
        })
        
    except ValueError as e:
        if "No matching object found" in str(e):
            return jsonify({"error": str(e)}), 404
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@detection_bp.route("/face-crop", methods=["POST"])
def face_crop_endpoint():
    """
    Detects and crops faces from an image.
    Params: image or image_url, padding (optional int)
    """
    try:
        image, form = ImageUtils.load_image_from_request()
        padding = int(form.get('padding', 50))

        # Detect and crop face
        cropped = detection_service.face_crop(image, padding=padding)

        return jsonify({
            "success": True,
            "image": ImageUtils.image_to_base64(cropped)
        })
        
    except ValueError as e:
        if "No face detected" in str(e):
            return jsonify({"error": str(e)}), 404
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@detection_bp.route("/smart-crop", methods=["POST"])
def smart_crop_endpoint():
    """
    Performs smart cropping on an image.
    Params: image or image_url, width (int), height (int)
    """
    try:
        image, form = ImageUtils.load_image_from_request()
        
        # Get required parameters
        width = form.get('width')
        height = form.get('height')
        
        if not width or not height:
            return jsonify({"error": "Both 'width' and 'height' are required."}), 400
            
        width = int(width)
        height = int(height)

        # Perform smart crop
        cropped = detection_service.smart_crop(image, width, height)

        return jsonify({
            "success": True,
            "image": ImageUtils.image_to_base64(cropped)
        })
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@detection_bp.route("/detect-info", methods=["POST"])
def detect_info_endpoint():
    """
    Gets detection information without cropping.
    Params: image or image_url, prompt
    """
    try:
        image, form = ImageUtils.load_image_from_request()
        prompt = form.get('prompt')
        
        if not prompt:
            return jsonify({"error": "Prompt is required."}), 400

        # Get detection information
        detection_info = detection_service.get_detection_info(image, prompt)

        return jsonify({
            "success": True,
            **detection_info
        })
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500 