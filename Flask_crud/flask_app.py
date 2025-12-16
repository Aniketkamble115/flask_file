
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from datetime import timedelta
from extensions import db
from flask_sqlalchemy import SQLAlchemy
from resources.auth_resource import auth_bp
from resources.employee_resource import employee_bp

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Anii@123@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Swagger Configuration
app.config['SWAGGER'] = {
    'title': 'Employee Management API',
    'uiversion': 3,
    'version': '1.0',
    'description': 'Layered Architecture with DAO, Provider, and Resource layers'
}

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)
swagger = Swagger(app)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(employee_bp)

# Database initialization endpoint
@app.route('/api/init-db', methods=['POST'])
def init_db():
    """Initialize database tables"""
    try:
        with app.app_context():
            db.create_all()
        return jsonify({"message": "Database initialized successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return jsonify({
        "message": "Employee Management API",
        "docs": "/apidocs",
        "version": "1.0"
    })

if __name__ == '__main__':
    app.run(debug=True)