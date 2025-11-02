"""
Static Files Routes Blueprint
Handles serving static frontend files
"""
from flask import Blueprint, send_from_directory, current_app
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

# Create blueprint
static_bp = Blueprint('static', __name__)


@static_bp.route('/')
def index():
    """Serve main index.html"""
    return send_from_directory(Config.FRONTEND_DIR, 'index.html')


@static_bp.route('/<path:path>')
def serve_static(path):
    """Serve static files from frontend directory"""
    return send_from_directory(Config.FRONTEND_DIR, path)

