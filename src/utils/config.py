"""
Configuration management utilities for the Streamlit application.
"""
import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


def load_config(config_path: str = "configs/app_config.yaml"):
    config_file = Path(config_path)
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    return {"categories": {}}


# Global configuration instance
config = load_config() 