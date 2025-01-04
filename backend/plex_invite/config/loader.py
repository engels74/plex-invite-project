import yaml
from pathlib import Path
from typing import Optional
from .schema import AppConfig

class ConfigLoader:
    """Handles loading and saving configuration from/to YAML file"""
    
    def __init__(self, config_path: str = "config/config.yml"):
        self.config_path = Path(config_path)
        # Create config directory if it doesn't exist
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self._config: Optional[AppConfig] = None

    def load(self) -> AppConfig:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found at {self.config_path}")
            
        try:
            with open(self.config_path, 'r') as f:
                config_data = yaml.safe_load(f) or {}
            self._config = AppConfig(**config_data)
            return self._config
        except Exception as e:
            raise RuntimeError(f"Failed to load config: {str(e)}")

    def save(self, config: AppConfig) -> None:
        """Save configuration to YAML file"""
        try:
            with open(self.config_path, 'w') as f:
                yaml.safe_dump(config.model_dump(), f)
            self._config = config
        except Exception as e:
            raise RuntimeError(f"Failed to save config: {str(e)}")

    @property
    def config(self) -> AppConfig:
        """Get the current configuration"""
        if self._config is None:
            raise RuntimeError("Configuration not loaded")
        return self._config