"""
Configuration management for AR Galgame Assistant
All configuration parameters are loaded from environment variables or default values
"""
import os
from typing import Dict, Any

class Config:
    """Base configuration class"""
    
    # Base directories
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), 'frontend')
    
    # Flask configuration
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', '5000'))
    
    # Qwen API Configuration - loaded from environment variables
    QWEN_API_KEY = os.getenv('QWEN_API_KEY', 'sk-1ff3a1c15f884e31b3a7492748e37a97')
    QWEN_API_URL = os.getenv(
        'QWEN_API_URL', 
        'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation'
    )
    QWEN_MODEL = os.getenv('QWEN_MODEL', 'qwen-turbo')
    QWEN_TEMPERATURE = float(os.getenv('QWEN_TEMPERATURE', '0.7'))
    QWEN_MAX_TOKENS = int(os.getenv('QWEN_MAX_TOKENS', '200'))
    QWEN_TOP_P = float(os.getenv('QWEN_TOP_P', '0.8'))
    QWEN_TIMEOUT = int(os.getenv('QWEN_TIMEOUT', '15'))
    
    # API Request configuration
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', '15'))
    
    # Response generation configuration
    DEFAULT_FALLBACK_RESPONSES = [
        "好的，我理解了。",
        "没问题，我知道你的意思。",
        "明白了，我会注意的。"
    ]
    
    @classmethod
    def get_qwen_config(cls) -> Dict[str, Any]:
        """Get Qwen API configuration as dictionary"""
        return {
            'api_key': cls.QWEN_API_KEY,
            'api_url': cls.QWEN_API_URL,
            'model': cls.QWEN_MODEL,
            'temperature': cls.QWEN_TEMPERATURE,
            'max_tokens': cls.QWEN_MAX_TOKENS,
            'top_p': cls.QWEN_TOP_P,
            'timeout': cls.QWEN_TIMEOUT
        }
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration parameters"""
        if not cls.QWEN_API_KEY:
            print("Warning: QWEN_API_KEY is not set")
            return False
        if not cls.QWEN_API_URL:
            print("Warning: QWEN_API_URL is not set")
            return False
        if not os.path.exists(cls.FRONTEND_DIR):
            print(f"Warning: Frontend directory not found: {cls.FRONTEND_DIR}")
            return False
        return True
    
    @classmethod
    def print_config(cls):
        """Print current configuration (excluding sensitive data)"""
        print("=== Configuration ===")
        print(f"Frontend Directory: {cls.FRONTEND_DIR}")
        print(f"Flask Host: {cls.HOST}")
        print(f"Flask Port: {cls.PORT}")
        print(f"Debug Mode: {cls.DEBUG}")
        print(f"Qwen API URL: {cls.QWEN_API_URL}")
        print(f"Qwen Model: {cls.QWEN_MODEL}")
        print(f"Qwen Temperature: {cls.QWEN_TEMPERATURE}")
        print(f"Qwen Max Tokens: {cls.QWEN_MAX_TOKENS}")
        print(f"Qwen Top P: {cls.QWEN_TOP_P}")
        print(f"Qwen API Key: {'*' * 10 + cls.QWEN_API_KEY[-4:] if cls.QWEN_API_KEY else 'Not Set'}")
        print("===================")

