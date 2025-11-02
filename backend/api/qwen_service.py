"""
Qwen API Service Module
Handles all interactions with Qwen API
"""
import requests
import json
import sys
import os
from typing import List, Dict, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config


class QwenService:
    """Service class for Qwen API interactions"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Qwen service with configuration
        
        Args:
            config: Optional configuration dictionary. If None, uses Config.get_qwen_config()
        """
        self.config = config or Config.get_qwen_config()
        self.api_key = self.config['api_key']
        self.api_url = self.config['api_url']
        self.model = self.config['model']
        self.temperature = self.config['temperature']
        self.max_tokens = self.config['max_tokens']
        self.top_p = self.config['top_p']
        self.timeout = self.config['timeout']
    
    def generate_response_options(
        self,
        user_message: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        custom_prompt: Optional[str] = None
    ) -> List[str]:
        """
        Generate three response options using Qwen API
        
        Args:
            user_message: The message to generate responses for
            model: Optional model name (overrides config)
            temperature: Optional temperature (overrides config)
            max_tokens: Optional max tokens (overrides config)
            top_p: Optional top_p (overrides config)
            custom_prompt: Optional custom prompt template
        
        Returns:
            List of three response options
        """
        # Use provided parameters or fall back to config
        model = model or self.model
        temperature = temperature if temperature is not None else self.temperature
        max_tokens = max_tokens or self.max_tokens
        top_p = top_p if top_p is not None else self.top_p
        
        # Generate prompt
        prompt = self._generate_prompt(user_message, custom_prompt)
        
        # Prepare API request
        headers = self._build_headers()
        payload = self._build_payload(prompt, model, temperature, max_tokens, top_p)
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            
            print(f"Qwen API response: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            # Extract and parse response
            options = self._extract_options(result)
            if options and len(options) >= 3:
                return options[:3]
            else:
                print("Failed to extract valid options from API response, using fallback")
                return Config.DEFAULT_FALLBACK_RESPONSES.copy()
                
        except requests.exceptions.RequestException as e:
            print(f"Qwen API request error: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    print(f"API error details: {json.dumps(error_detail, ensure_ascii=False)}")
                except:
                    print(f"API error response: {e.response.text}")
            return Config.DEFAULT_FALLBACK_RESPONSES.copy()
        except Exception as e:
            print(f"Unexpected error in QwenService: {str(e)}")
            import traceback
            traceback.print_exc()
            return Config.DEFAULT_FALLBACK_RESPONSES.copy()
    
    def _generate_prompt(self, user_message: str, custom_prompt: Optional[str] = None) -> str:
        """Generate prompt for Qwen API"""
        if custom_prompt:
            return custom_prompt.format(user_message=user_message)
        
        return f"""你是一个高情商的沟通助手。当有人对你说："{user_message}"

请生成恰好三个回复选项。每个回复应该：
1. 日常且简洁（不超过20字）
2. 高情商且合适
3. 自然且符合人类说话习惯

请以JSON数组格式返回，包含恰好三个字符串，例如：
["回复选项1", "回复选项2", "回复选项3"]

只返回JSON数组，不要其他内容："""
    
    def _build_headers(self) -> Dict[str, str]:
        """Build HTTP headers for API request"""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'X-DashScope-API-Key': self.api_key,  # Alternative header format
            'Content-Type': 'application/json'
        }
    
    def _build_payload(
        self,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
        top_p: float
    ) -> Dict[str, Any]:
        """Build API request payload"""
        return {
            "model": model,
            "input": {
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            "parameters": {
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p
            }
        }
    
    def _extract_options(self, api_response: Dict[str, Any]) -> Optional[List[str]]:
        """Extract response options from API response"""
        generated_text = None
        
        # Format 1: output.choices[0].message.content
        if 'output' in api_response:
            output = api_response['output']
            if 'choices' in output and len(output['choices']) > 0:
                if 'message' in output['choices'][0] and 'content' in output['choices'][0]['message']:
                    generated_text = output['choices'][0]['message']['content'].strip()
        
        # Format 2: output.text or output.texts
        if not generated_text and 'output' in api_response:
            output = api_response['output']
            if 'text' in output:
                generated_text = output['text'].strip()
            elif 'texts' in output and len(output['texts']) > 0:
                generated_text = output['texts'][0].strip()
        
        # Format 3: direct text field
        if not generated_text and 'text' in api_response:
            generated_text = api_response['text'].strip()
        
        if not generated_text:
            return None
        
        # Try to parse JSON from the response
        generated_text = generated_text.replace('```json', '').replace('```', '').strip()
        
        try:
            # Try to parse as JSON
            options = json.loads(generated_text)
            if isinstance(options, list) and len(options) >= 3:
                return options[:3]
            elif isinstance(options, list) and len(options) > 0:
                # Pad with fallbacks if needed
                while len(options) < 3:
                    options.append(Config.DEFAULT_FALLBACK_RESPONSES[len(options)])
                return options[:3]
        except json.JSONDecodeError:
            # If not valid JSON, try to extract three options manually
            options = self._extract_options_from_text(generated_text)
            if options and len(options) >= 3:
                return options[:3]
            elif options and len(options) > 0:
                # Pad with fallbacks if needed
                while len(options) < 3:
                    options.append(Config.DEFAULT_FALLBACK_RESPONSES[len(options)])
                return options[:3]
        
        return None
    
    def _extract_options_from_text(self, text: str) -> List[str]:
        """Extract three response options from text if JSON parsing fails"""
        options = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # Remove list markers (1., 2., 3., -, *, etc.)
            for marker in ['1.', '2.', '3.', '-', '*', '"', "'"]:
                if line.startswith(marker):
                    line = line[len(marker):].strip()
            # Remove quotes if present
            line = line.strip('"').strip("'")
            if line and len(options) < 3:
                options.append(line)
        
        return options[:3]

