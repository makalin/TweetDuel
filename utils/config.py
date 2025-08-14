"""
Configuration utilities for TweetDuel
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any

def get_config_path() -> Path:
    """Get the default configuration file path"""
    return Path.home() / '.tweetduel' / 'config.yaml'

def load_config(config_path: str = None) -> Dict[str, Any]:
    """Load configuration from file"""
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    # Try default path
    default_path = get_config_path()
    if default_path.exists():
        with open(default_path, 'r') as f:
            return yaml.safe_load(f)
    
    return get_default_config()

def get_default_config() -> Dict[str, Any]:
    """Get default configuration"""
    return {
        'ai': {
            'model': 'llama3.2',
            'temperature': 0.8,
            'max_tokens': 500
        },
        'scraping': {
            'max_replies': 50,
            'include_quotes': True,
            'language_filter': 'en'
        },
        'debate': {
            'default_persona': 'socrates',
            'response_styles': ['contrarian', 'devils_advocate', 'nuanced'],
            'viral_hooks': True
        },
        'ollama_host': 'http://localhost:11434'
    }

def save_config(config: Dict[str, Any], config_path: str = None) -> None:
    """Save configuration to file"""
    if not config_path:
        config_path = get_config_path()
    
    # Ensure directory exists
    Path(config_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, indent=2)

def create_default_config() -> None:
    """Create default configuration file"""
    config = get_default_config()
    save_config(config)
