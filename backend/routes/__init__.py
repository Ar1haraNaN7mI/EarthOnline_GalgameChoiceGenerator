"""
Routes package initialization
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routes.static_routes import static_bp

__all__ = ['static_bp']

