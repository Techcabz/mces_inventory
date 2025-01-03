import os

class Config:
    # API Configuration
    API_URL = os.getenv("API_URL", "")  
    API_KEY = os.getenv("API_KEY", "")  
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")  

    # General Configurations
    SESSION_COOKIE_SECURE = True  
    JSON_SORT_KEYS = False 
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  



class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    TEMPLATES_AUTO_RELOAD = True

class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'
    SESSION_COOKIE_SECURE = True
  