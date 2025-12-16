from flask import Flask
from extensions.db import db
from flask_jwt_extended import JWTManager
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    JWTManager(app)

    # Register Blueprints
    from resources.auth_resource import auth_bp
    from resources.employee_resource import employee_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(employee_bp)

    return app
