import os

class Config:
    """Configuration class for the Flask app."""
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/avatars')
    
    # BlueSky login credentials
    BLUESKY_HANDLE = os.getenv('BLUESKY_HANDLE', 'sparrow.0x0e.top')
    BLUESKY_PASSWORD = os.getenv('BLUESKY_PASSWORD', 'Hdz20070225')
    BLUESKY_BASE = os.getenv('BLUESKY_BASE', 'https://0x0e.top')