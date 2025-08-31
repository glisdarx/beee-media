"""
应用配置文件
"""

import os
from typing import Dict, Any

class Config:
    """基础配置"""
    
    # Flask配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-this')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # JWT配置
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-change-this')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', '86400'))  # 24小时
    
    # Supabase配置
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')
    SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
    
    # SendGrid配置
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    SENDGRID_FROM_EMAIL = os.getenv('SENDGRID_FROM_EMAIL', 'noreply@beeemedia.com')
    SENDGRID_FROM_NAME = os.getenv('SENDGRID_FROM_NAME', 'Beee Media')
    
    # Google OAuth配置
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    
    # TikHub API配置
    TIKHUB_API_KEY = os.getenv('TIKHUB_API_KEY', 'w7MRRTtG50I0nQQRwUXvkCUdwyZXk5mI4alf2QvjknZZ4XIzYNAv/kK8AA==')
    TIKHUB_BASE_URL = os.getenv('TIKHUB_BASE_URL', 'https://api.tikhub.io')
    
    # CORS配置
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'https://beeemedia.com,https://*.beeemedia.com,https://*.pages.dev').split(',')
    
    # 速率限制配置
    RATELIMIT_STORAGE_URL = os.getenv('REDIS_URL', 'memory://')
    RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT', '100 per hour')
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', '16777216'))  # 16MB
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    
    # 日志配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')
    
    # 分页配置
    DEFAULT_PAGE_SIZE = int(os.getenv('DEFAULT_PAGE_SIZE', '20'))
    MAX_PAGE_SIZE = int(os.getenv('MAX_PAGE_SIZE', '100'))
    
    # 缓存配置
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', '300'))
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """验证配置"""
        errors = []
        warnings = []
        
        # 可选但推荐的配置项
        optional_configs = {
            'SUPABASE_URL': cls.SUPABASE_URL,
            'SUPABASE_ANON_KEY': cls.SUPABASE_ANON_KEY,
            'SENDGRID_API_KEY': cls.SENDGRID_API_KEY,
            'GOOGLE_CLIENT_ID': cls.GOOGLE_CLIENT_ID,
            'JWT_SECRET_KEY': cls.JWT_SECRET_KEY,
        }
        
        for key, value in optional_configs.items():
            if not value or value.startswith(('dev-', 'jwt-', 'change-this')):
                warnings.append(f"Recommended configuration missing or using default: {key}")
        
        return {
            'valid': True,  # 所有配置都是可选的
            'errors': errors,
            'warnings': warnings
        }
    
    @classmethod
    def get_config_summary(cls) -> Dict[str, Any]:
        """获取配置摘要（不包含敏感信息）"""
        return {
            'debug': cls.DEBUG,
            'supabase_configured': bool(cls.SUPABASE_URL and cls.SUPABASE_ANON_KEY),
            'sendgrid_configured': bool(cls.SENDGRID_API_KEY),
            'google_oauth_configured': bool(cls.GOOGLE_CLIENT_ID),
            'tikhub_configured': bool(cls.TIKHUB_API_KEY),
            'cors_origins': cls.CORS_ORIGINS,
            'log_level': cls.LOG_LEVEL,
            'max_page_size': cls.MAX_PAGE_SIZE,
            'cache_type': cls.CACHE_TYPE
        }

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """测试环境配置"""
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False

# 根据环境变量选择配置
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """获取当前配置"""
    env = os.getenv('FLASK_ENV', 'default')
    return config_map.get(env, DevelopmentConfig)