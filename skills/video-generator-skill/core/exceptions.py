"""
Custom Exception Classes

Design Principles:
1. Hierarchical exception system
2. Context-rich exceptions
3. Bilingual support (En/Cn)
"""


class SkillError(Exception):
    """
    Base Skill Exception
    All custom exceptions inherit from this class
    """
    
    def __init__(self, message: str, message_cn: str = None, details: dict = None):
        """
        Initialize exception
        
        Args:
            message: English error message
            message_cn: Chinese error message (optional)
            details: Extra details (optional)
        """
        super().__init__(message)
        self.message = message
        self.message_cn = message_cn or message
        self.details = details or {}
    
    def __str__(self):
        return f"{self.message_cn} ({self.message})"
    
    def to_dict(self) -> dict:
        """Convert to dict for logging"""
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "message_cn": self.message_cn,
            "details": self.details
        }


class ConfigError(SkillError):
    """
    Configuration Error
    - API Key missing
    - Config format invalid
    - Env var missing
    """
    
    def __init__(self, key: str, message: str = None, message_cn: str = None):
        message = message or f"Configuration error: {key} is not set or invalid"
        message_cn = message_cn or f"配置错误: {key} 未设置或无效"
        super().__init__(
            message=message,
            message_cn=message_cn,
            details={"config_key": key}
        )
        self.key = key


class NetworkError(SkillError):
    """
    Network Error
    - Connection timeout
    - DNS resolution failed
    - Service unavailable
    """
    
    def __init__(self, url: str = None, message: str = None, message_cn: str = None, 
                 status_code: int = None):
        message = message or f"Network error occurred"
        message_cn = message_cn or f"网络错误"
        super().__init__(
            message=message,
            message_cn=message_cn,
            details={"url": url, "status_code": status_code}
        )
        self.url = url
        self.status_code = status_code


class AuthError(SkillError):
    """
    Authentication Error
    - API Key invalid
    - Token expired
    - Permission denied
    """
    
    def __init__(self, service: str, message: str = None, message_cn: str = None):
        message = message or f"Authentication failed for {service}"
        message_cn = message_cn or f"{service} 认证失败"
        super().__init__(
            message=message,
            message_cn=message_cn,
            details={"service": service}
        )
        self.service = service


class DependencyError(SkillError):
    """
    Dependency Error
    - Python package missing
    - System tool missing
    """
    
    def __init__(self, dependency: str, install_cmd: str = None, 
                 message: str = None, message_cn: str = None):
        message = message or f"Dependency '{dependency}' is not installed"
        message_cn = message_cn or f"依赖 '{dependency}' 未安装"
        
        details = {"dependency": dependency}
        if install_cmd:
            details["install_command"] = install_cmd
            message_cn += f"，请运行: {install_cmd}"
        
        super().__init__(
            message=message,
            message_cn=message_cn,
            details=details
        )
        self.dependency = dependency
        self.install_cmd = install_cmd


class ValidationError(SkillError):
    """
    Validation Error
    - Invalid format
    - Illegal input
    """
    
    def __init__(self, field: str, value: any = None, 
                 message: str = None, message_cn: str = None):
        message = message or f"Validation failed for field '{field}'"
        message_cn = message_cn or f"参数 '{field}' 验证失败"
        super().__init__(
            message=message,
            message_cn=message_cn,
            details={"field": field, "value": str(value)[:100]}  # Truncate long values
        )
        self.field = field
        self.value = value
