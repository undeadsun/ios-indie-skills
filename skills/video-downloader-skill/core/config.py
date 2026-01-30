"""
Configuration Management Module

Features:
1. Load config from environment variables
2. Support .env file
3. Configuration validation
4. Default value management
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, field

from .exceptions import ConfigError


# dotenv
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False


@dataclass
class Config:
    """
    Configuration Management Class
    
    Usage:
        config = Config.load()
        api_key = config.get("MY_API_KEY")
    """
    
    # Skill directory path
    skill_dir: Path = field(default_factory=lambda: Path(__file__).parent.parent)
    
    # Output directory
    output_dir: Path = None
    
    # Cache directory
    cache_dir: Path = None
    
    # Environment variable cache
    _env_cache: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        """Post-initialization processing"""
        # Set default directories
        if self.output_dir is None:
            self.output_dir = self.skill_dir / "downloads"
        if self.cache_dir is None:
            self.cache_dir = self.skill_dir / "cache"
        
        # Ensure directories exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def load(cls, env_file: Optional[Path] = None) -> "Config":
        """
        Load configuration
        
        Args:
            env_file: .env file path (optional)
            
        Returns:
            Config instance
        """
        # Try loading .env file
        if DOTENV_AVAILABLE:
            if env_file and env_file.exists():
                load_dotenv(env_file)
            else:
                # Try loading from skill directory
                skill_dir = Path(__file__).parent.parent
                default_env = skill_dir / ".env"
                if default_env.exists():
                    load_dotenv(default_env)
        
        return cls()
    
    def get(self, key: str, default: Any = None, required: bool = False) -> Optional[str]:
        """
        Get configuration value
        
        Args:
            key: Config key
            default: Default value
            required: Is required (raises exception if True and missing)
            
        Returns:
            Config value
            
        Raises:
            ConfigError: If required=True and value missing
        """
        # Prefer cache
        if key in self._env_cache:
            return self._env_cache[key]
        
        # Get from environment
        value = os.environ.get(key)
        
        if value is None:
            if required:
                raise ConfigError(
                    key=key,
                    message=f"Required configuration '{key}' is not set",
                )
            return default
        
        # Cache and return
        self._env_cache[key] = value
        return value
    
    def set(self, key: str, value: str, persist: bool = False):
        """
        Set configuration value
        
        Args:
            key: Config key
            value: Config value
            persist: Persist to .env file
        """
        os.environ[key] = value
        self._env_cache[key] = value
        
        if persist:
            self._persist_to_env(key, value)
    
    def _persist_to_env(self, key: str, value: str):
        """Persist config to .env file"""
        env_file = self.skill_dir / ".env"
        
        # Read existing content
        lines = []
        if env_file.exists():
            with open(env_file, "r") as f:
                lines = f.readlines()
        
        # Find and update or append
        key_found = False
        for i, line in enumerate(lines):
            if line.startswith(f"{key}="):
                lines[i] = f'{key}="{value}"\n'
                key_found = True
                break
        
        if not key_found:
            lines.append(f'{key}="{value}"\n')
        
        # Write back to file
        with open(env_file, "w") as f:
            f.writelines(lines)
    
    def validate(self, required_keys: list) -> Dict[str, bool]:
        """
        Validate required configuration items
        
        Args:
            required_keys: List of required config keys
            
        Returns:
            Validation results dict {key: is_valid}
        """
        results = {}
        for key in required_keys:
            value = self.get(key)
            results[key] = value is not None and len(value.strip()) > 0
        return results
    
    def status(self) -> Dict[str, Any]:
        """
        Get configuration status summary
        
        Returns:
            Status dictionary
        """
        return {
            "skill_dir": str(self.skill_dir),
            "output_dir": str(self.output_dir),
            "cache_dir": str(self.cache_dir),
            "dotenv_available": DOTENV_AVAILABLE,
            "env_file_exists": (self.skill_dir / ".env").exists(),
        }


# Global config instance (lazy loaded)
_config_instance: Optional[Config] = None


def get_config() -> Config:
    """Get global config instance"""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config.load()
    return _config_instance
