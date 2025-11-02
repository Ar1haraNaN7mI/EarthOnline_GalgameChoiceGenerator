"""
Main Flask Application
Uses Blueprint architecture for modular routing
"""
from flask import Flask
from flask_cors import CORS
import os
import sys

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from config import Config
from api.routes import api_bp
from routes.static_routes import static_bp


def create_app(config_class=Config):
    """
    Application factory function
    Creates and configures Flask application instance
    
    Args:
        config_class: Configuration class to use
    
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(static_bp)
    app.register_blueprint(api_bp)
    
    # Validate configuration
    if not config_class.validate_config():
        print("Warning: Configuration validation failed")
    
    return app


# Create application instance
app = create_app(Config)


@app.before_request
def setup():
    """Setup function called before each request"""
    # Ensure frontend directory exists
    if not os.path.exists(Config.FRONTEND_DIR):
        os.makedirs(Config.FRONTEND_DIR)
        print(f"Created frontend directory: {Config.FRONTEND_DIR}")


if __name__ == '__main__':
    # Print configuration
    Config.print_config()
    
    # Ensure frontend directory exists
    if not os.path.exists(Config.FRONTEND_DIR):
        os.makedirs(Config.FRONTEND_DIR)
        print(f"Created frontend directory: {Config.FRONTEND_DIR}")
    
    print(f"\nStarting server at http://{Config.HOST}:{Config.PORT}")
    print(f"Frontend directory: {Config.FRONTEND_DIR}\n")
    
    app.run(
        debug=Config.DEBUG,
        host=Config.HOST,
        port=Config.PORT
    )
