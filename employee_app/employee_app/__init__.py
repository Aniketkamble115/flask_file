from flask import Flask
from flask_restx import Api
from employee_app.config import Config
from employee_app.extensions.db import db
from employee_app.extensions.bcrypt import bcrypt
from employee_app.extensions.jwt import jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # JWT Security for Swagger UI
    authorizations = {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Use: Bearer <access_token>'
        }
    }

    api = Api(
        app,
        version='1.0',
        title='Employee API',
        description='Employee CRUD API with JWT Authentication',
        doc='/', 
        security='Bearer',      # ← default security
        authorizations=authorizations  # ← add authorize button
    )

    from employee_app.routes.auth_routes import auth_ns
    from employee_app.routes.employee_routes import employee_ns
    
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(employee_ns, path='/employees')

    return app
