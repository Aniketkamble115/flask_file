from flask import Blueprint, request, jsonify
from providers.auth_provider import AuthProvider
from schemas.user_schema import user_registration_schema, user_login_schema
from marshmallow import ValidationError
from flasgger import swag_from

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
@swag_from({
    "tags": ["Authentication"],
    "description": "Register a new user",
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "parameters": [{
        "name": "body",
        "in": "body",
        "required": True,
        "schema": {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "email": {"type": "string"},
                "password": {"type": "string"}
            }
        }
    }],
    "responses": {
        201: {"description": "User registered successfully"},
        400: {"description": "Validation error or user already exists"}
    }
})
def register():
    """Register a new user"""
    try:
        data = user_registration_schema.load(request.json)
        result = AuthProvider.register_user(data)
        return jsonify(result), 201

    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    except ValueError as e:
        return jsonify({"error": str(e)}), 400



@auth_bp.route("/login", methods=["POST"])
@swag_from({
    "tags": ["Authentication"],
    "description": "Login and get JWT token",
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "parameters": [{
        "name": "body",
        "in": "body",
        "required": True,
        "schema": {
            "type": "object",
            "properties": {
                "email": {"type": "string"},
                "password": {"type": "string"}
            }
        }
    }],
    "responses": {
        200: {"description": "User authenticated successfully"},
        401: {"description": "Invalid login credentials"},
        400: {"description": "Validation error"}
    }
})
def login():
    """Login user"""
    try:
        data = user_login_schema.load(request.json)
        result = AuthProvider.login_user(data)
        return jsonify(result), 200

    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    except ValueError as e:
        return jsonify({"error": str(e)}), 401
