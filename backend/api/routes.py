"""
API Routes Blueprint
Handles all API endpoints
"""
from flask import Blueprint, request, jsonify, current_app
import sys
import os
from typing import Dict, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.qwen_service import QwenService
from config import Config

# Create blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/generate-responses', methods=['POST'])
def generate_responses():
    """
    Receive transcribed text and generate three response options using Qwen API
    
    Request Body:
    {
        "message": "user message text",
        "model": "qwen-turbo" (optional),
        "temperature": 0.7 (optional),
        "max_tokens": 200 (optional),
        "top_p": 0.8 (optional),
        "custom_prompt": "custom prompt template" (optional),
        "api_key": "custom api key" (optional),
        "api_url": "custom api url" (optional)
    }
    
    Response:
    {
        "success": true,
        "options": ["option1", "option2", "option3"]
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        user_message = data.get('message', '').strip()
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Extract parameters from request or use defaults
        model = data.get('model')
        temperature = data.get('temperature')
        max_tokens = data.get('max_tokens')
        top_p = data.get('top_p')
        custom_prompt = data.get('custom_prompt')
        
        # Get API configuration - allow override from request
        qwen_config = Config.get_qwen_config()
        if 'api_key' in data:
            qwen_config['api_key'] = data['api_key']
        if 'api_url' in data:
            qwen_config['api_url'] = data['api_url']
        
        # Initialize Qwen service with configuration
        qwen_service = QwenService(config=qwen_config)
        
        # Generate response options with provided parameters
        responses = qwen_service.generate_response_options(
            user_message=user_message,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            custom_prompt=custom_prompt
        )
        
        return jsonify({
            'success': True,
            'options': responses,
            'message': user_message
        })
    
    except Exception as e:
        current_app.logger.error(f"Error in generate_responses: {str(e)}")
        import traceback
        current_app.logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500


@api_bp.route('/config', methods=['GET'])
def get_config():
    """
    Get current API configuration (excluding sensitive data)
    
    Response:
    {
        "api_url": "...",
        "model": "...",
        "temperature": 0.7,
        "max_tokens": 200,
        "top_p": 0.8
    }
    """
    config = Config.get_qwen_config()
    return jsonify({
        'api_url': config['api_url'],
        'model': config['model'],
        'temperature': config['temperature'],
        'max_tokens': config['max_tokens'],
        'top_p': config['top_p'],
        'timeout': config['timeout']
    })


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'AR Galgame Assistant API'
    })

