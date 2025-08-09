"""
Basic tests for AutoRender AI Flask application
"""

import pytest
from autorender_ai import create_app


@pytest.fixture
def app():
    """Create and configure a test app"""
    app = create_app('development')
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()


def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'status' in data
    assert 'version' in data
    assert data['status'] == 'AutoRender AI API running'


def test_status_endpoint(client):
    """Test the status endpoint"""
    response = client.get('/status')
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'status' in data
    assert 'models' in data
    assert 'endpoints' in data


def test_root_endpoint(client):
    """Test the root endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'status' in data


def test_missing_image_endpoints(client):
    """Test endpoints with missing image data"""
    # Test remove-bg endpoint
    response = client.post('/remove-bg')
    assert response.status_code == 400
    
    # Test detect endpoint
    response = client.post('/detect')
    assert response.status_code == 400
    
    # Test swap-background endpoint  
    response = client.post('/swap-background')
    assert response.status_code == 400 