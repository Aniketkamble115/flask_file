from flask import Flask
from flask_restx import Api
from config import Config
from extensions.db import db
from extensions.bcrypt import bcrypt
from extensions.jwt import jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Initialize Flask-RESTX API
    api = Api(
        app,
        version='1.0',
        title='Employee API',
        description='Employee CRUD API',
        doc='/'  # Swagger UI at root
    )

    # Import and register ALL namespaces
    from routes.auth_routes import auth_ns
    from routes.employee_routes import employee_ns
    
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(employee_ns, path='/employees')

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)