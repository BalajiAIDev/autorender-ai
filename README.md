# AutoRender AI - Image Processing Microservice

A powerful Flask-based microservice for AI-powered image processing including background removal, AI-generated background replacement, object detection, and smart cropping.

## 🌟 Features

- 🎨 **Background Removal** with edge refinement
- 🌟 **AI Background Generation** using Stable Diffusion
- 🔍 **Object Detection** and cropping with YOLO
- 👤 **Face Detection** and cropping
- 🧠 **Smart Cropping** for optimal image composition
- ⚡ **GPU Acceleration** support
- 🌐 **RESTful API** with JSON responses
- 🔧 **Easy Deployment** with Docker and Colab support

## 📋 Requirements

- Python 3.8+
- CUDA-capable GPU (recommended)
- 4GB+ RAM
- 10GB+ free disk space (for AI models)

## 🚀 Quick Start

### Option 1: Google Colab (Recommended for Testing)

1. Open the `colab_quickstart.ipynb` notebook in Google Colab
2. Run all cells to automatically setup and start the service
3. Get a public URL via ngrok tunnel

### Option 2: Local Installation

```bash
# Clone the repository
git clone https://github.com/your-username/autorender-ai.git
cd autorender-ai

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Option 3: Package Installation

```bash
# Install as a package
pip install -e .

# Import and use
from autorender_ai import create_app
app = create_app()
app.run()
```

## 📁 Project Structure

```
autorender-ai/
├── autorender_ai/              # Main package
│   ├── __init__.py             # Package initialization
│   ├── app.py                  # Flask application factory
│   ├── config.py               # Configuration management
│   ├── models/                 # AI model management
│   │   ├── __init__.py
│   │   └── ai_models.py        # Model loading and initialization
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── background_service.py    # Background processing
│   │   ├── detection_service.py     # Object detection
│   │   └── image_utils.py           # Image utilities
│   ├── routes/                 # API endpoints
│   │   ├── __init__.py
│   │   ├── background_routes.py     # Background endpoints
│   │   ├── detection_routes.py      # Detection endpoints
│   │   └── health_routes.py         # Health/status endpoints
│   └── utils/                  # Utility functions
├── tests/                      # Test suite
├── colab_quickstart.ipynb      # Colab setup notebook
├── colab_validator.ipynb       # Validation notebook
├── app.py                      # Main application entry point
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🔧 Configuration

### Environment Variables

```bash
# Flask settings
FLASK_ENV=development           # development, production, colab
FLASK_DEBUG=true               # Enable debug mode
HOST=0.0.0.0                   # Server host
PORT=5000                      # Server port

# Ngrok settings (for Colab)
ENABLE_NGROK=false             # Enable ngrok tunnel
NGROK_AUTH_TOKEN=your_token    # Ngrok auth token
```

### Configuration Classes

- `DevelopmentConfig`: For local development
- `ProductionConfig`: For production deployment  
- `ColabConfig`: For Google Colab with ngrok

## 📚 API Documentation

### Authentication
No authentication required for this microservice.

### Base URL
- Local: `http://localhost:5000`
- Colab: `https://your-ngrok-url.ngrok.io`

### Endpoints

#### Health Check
```http
GET /health
GET /
```
**Response:**
```json
{
  "status": "AutoRender AI API running",
  "version": "1.0.0",
  "service": "autorender-ai"
}
```

#### System Status
```http
GET /status
```
**Response:**
```json
{
  "status": "running",
  "version": "1.0.0",
  "models": {
    "yolo": true,
    "stable_diffusion": true,
    "smart_crop": true,
    "device": "cuda"
  },
  "endpoints": {
    "background": ["/remove-bg", "/swap-background"],
    "detection": ["/detect", "/face-crop", "/smart-crop"],
    "health": ["/", "/health", "/status"]
  }
}
```

#### Background Removal
```http
POST /remove-bg
```
**Parameters:**
- `image`: Image file (multipart/form-data) OR
- `image_url`: Image URL (JSON)
- `bg_color`: Background color (hex, optional)
- `edge_blur_radius`: Edge blur radius (int, optional)

**Example:**
```bash
curl -X POST -F 'image=@photo.jpg' -F 'bg_color=#ffffff' http://localhost:5000/remove-bg
```

**Response:**
```json
{
  "success": true,
  "image": "base64_encoded_image_data"
}
```

#### AI Background Replacement
```http
POST /swap-background
```
**Parameters:**
- `image`: Image file (multipart/form-data) OR
- `image_url`: Image URL (JSON)
- `prompt`: AI generation prompt (required)
- `width`: Target width (int, optional)
- `height`: Target height (int, optional)

**Example:**
```bash
curl -X POST -F 'image=@photo.jpg' -F 'prompt=beautiful sunset beach' http://localhost:5000/swap-background
```

#### Object Detection & Cropping
```http
POST /detect
```
**Parameters:**
- `image`: Image file (multipart/form-data) OR
- `image_url`: Image URL (JSON)
- `prompt`: Object to detect (required)

**Example:**
```bash
curl -X POST -F 'image=@photo.jpg' -F 'prompt=person' http://localhost:5000/detect
```

#### Face Detection & Cropping
```http
POST /face-crop
```
**Parameters:**
- `image`: Image file (multipart/form-data) OR
- `image_url`: Image URL (JSON)
- `padding`: Padding around face (int, optional, default: 50)

#### Smart Cropping
```http
POST /smart-crop
```
**Parameters:**
- `image`: Image file (multipart/form-data) OR
- `image_url`: Image URL (JSON)
- `width`: Target width (required)
- `height`: Target height (required)

#### Detection Information
```http
POST /detect-info
```
Get detection information without cropping.

**Response:**
```json
{
  "success": true,
  "detections": [
    {
      "bbox": [x0, y0, x1, y1],
      "confidence": 0.95,
      "class": "person"
    }
  ],
  "count": 1
}
```

## 🧪 Testing

### Run Validator Notebook
Open `colab_validator.ipynb` in Colab or Jupyter to run comprehensive validation tests.

### Local Testing
```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_app.py::test_health_endpoint -v
```

### Manual Testing
```python
from autorender_ai import create_app

app = create_app('development')
with app.test_client() as client:
    response = client.get('/health')
    print(response.get_json())
```

## 🐳 Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

## 🔍 Troubleshooting

### Common Issues

1. **GPU Not Detected**
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

2. **Model Loading Errors**
   - Ensure sufficient disk space (10GB+)
   - Check internet connection for model downloads
   - Verify CUDA compatibility

3. **Import Errors**
   ```bash
   pip install -r requirements.txt
   ```

4. **Memory Issues**
   - Reduce image sizes
   - Use CPU mode: `CUDA_VISIBLE_DEVICES=""`
   - Close other applications

### Debug Mode
```bash
FLASK_DEBUG=true python app.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and add tests
4. Run the validator notebook
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Stable Diffusion](https://github.com/huggingface/diffusers) for AI background generation
- [YOLO](https://github.com/ultralytics/ultralytics) for object detection
- [RemBG](https://github.com/danielgatis/rembg) for background removal
- [SmartCrop](https://github.com/jwagner/smartcrop.py) for intelligent cropping

## 📞 Support

- 🐛 [Report Issues](https://github.com/your-username/autorender-ai/issues)
- 💬 [Discussions](https://github.com/your-username/autorender-ai/discussions)
- 📧 Email: support@autorender.ai

---

**Made with ❤️ for the AI community** 