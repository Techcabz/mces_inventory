import os
from flask import Flask
from flask_login import LoginManager
from config import DevelopmentConfig, ProductionConfig
from .models.user_models import User


def create_app():
    app = Flask(__name__)
    
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # Register blueprints
    from app.views.main import main
    from app.views.admin import admin
    app.register_blueprint(main)
    app.register_blueprint(admin)


  
    return app
