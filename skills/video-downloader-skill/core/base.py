"""
Abstract Base Class Module

Provides unified handler interface for extension and maintenance
"""

import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List

from .config import Config, get_config
from .exceptions import SkillError


class BaseHandler(ABC):
    """
    Handler Base Class
    
    All specific handlers should inherit from this class and implement necessary methods
    
    Example:
        class MyHandler(BaseHandler):
            @property
            def name(self) -> str:
                return "my-handler"
            
            def execute(self, **kwargs) -> Dict[str, Any]:
                # Implement logic
                return {"status": "success"}
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize handler
        
        Args:
            config: Config instance (optional, uses global config if not provided)
        """
        self.config = config or get_config()
        self.logger = logging.getLogger(self.name)
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Handler name, for logging and identification"""
        pass
    
    @property
    def required_config_keys(self) -> List[str]:
        """
        Required configuration keys
        Subclasses can override this property to declare required config
        """
        return []
    
    @property
    def required_dependencies(self) -> List[Dict[str, str]]:
        """
        Required dependencies list
        Format: [{"name": "tool", "check_cmd": "tool --version", "install_cmd": "pip install tool"}]
        """
        return []
    
    def validate_config(self) -> bool:
        """
        Validate configuration completeness
        
        Returns:
            Validation passed
        """
        if not self.required_config_keys:
            return True
        
        results = self.config.validate(self.required_config_keys)
        missing = [k for k, v in results.items() if not v]
        
        if missing:
            self.logger.warning(f"Missing config items: {', '.join(missing)}")
            return False
        
        return True
    
    def check_dependencies(self) -> Dict[str, bool]:
        """
        Check if dependencies are installed
        
        Returns:
            Check results {dependency_name: is_available}
        """
        import subprocess
        
        results = {}
        for dep in self.required_dependencies:
            name = dep.get("name", "unknown")
            check_cmd = dep.get("check_cmd", f"{name} --version")
            
            try:
                result = subprocess.run(
                    check_cmd.split(),
                    capture_output=True,
                    timeout=5
                )
                results[name] = result.returncode == 0
            except (FileNotFoundError, subprocess.TimeoutExpired):
                results[name] = False
        
        return results
    
    def pre_execute(self, **kwargs) -> bool:
        """
        Preparation before execution
        
        Can be used for:
        - Validate arguments
        - Check preconditions
        - Initialize resources
        
        Returns:
            Preparation success
        """
        return True
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute core logic
        
        Args:
            **kwargs: Execution arguments
            
        Returns:
            Execution result dict
        """
        pass
    
    def post_execute(self, result: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        Cleanup after execution
        
        Can be used for:
        - Cleanup temporary files
        - Log statistics
        - Send notifications
        
        Args:
            result: Result from execute()
            
        Returns:
            Processed result
        """
        return result
    
    def run(self, **kwargs) -> Dict[str, Any]:
        """
        Complete execution flow (Template Method pattern)
        
        Order: pre_execute -> execute -> post_execute
        
        Args:
            **kwargs: Execution arguments
            
        Returns:
            Execution result
        """
        try:
            # Pre-execution check
            if not self.pre_execute(**kwargs):
                return {"success": False, "error": "Pre-execution check failed"}
            
            # Execute core logic
            result = self.execute(**kwargs)
            
            # Post-execution processing
            result = self.post_execute(result, **kwargs)
            
            return result
            
        except SkillError as e:
            self.logger.error(f"Execution error: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_details": e.to_dict()
            }
        except Exception as e:
            self.logger.exception(f"Unexpected error: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    def status(self) -> Dict[str, Any]:
        """
        Get handler status
        
        Returns:
            Status info dict
        """
        config_valid = self.validate_config()
        dependencies = self.check_dependencies()
        
        return {
            "name": self.name,
            "config_valid": config_valid,
            "dependencies": dependencies,
            "ready": config_valid and all(dependencies.values())
        }
