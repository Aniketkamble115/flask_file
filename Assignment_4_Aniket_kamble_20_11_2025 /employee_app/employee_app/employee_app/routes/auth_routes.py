from flask_restx import Namespace, Resource, fields
from flask import request
from employee_app.dao.user_dao import UserDAO
from datetime import timedelta
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_required, 
    get_jwt_identity
)

auth_ns = Namespace("auth", description="Authentication")

# Models for Swagger
login_model = auth_ns.model('Login', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})

register_model = auth_ns.model('Register', {
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password')
})


@auth_ns.route("/register")
class Register(Resource):
    @auth_ns.expect(register_model)
    def post(self):
        """Register a new user"""
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # Validation
        if not username or not email or not password:
            return {'message': 'Missing required fields'}, 400
        
        # Check if user already exists
        if UserDAO.get_by_username(username):
            return {'message': 'Username already exists'}, 400
        
        if UserDAO.get_by_email(email):
            return {'message': 'Email already exists'}, 400
        
        # Create user
        try:
            user = UserDAO.create(username, email, password)
            return {
                'message': 'User created successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }, 201
        except Exception as e:
            return {'message': f'Error creating user: {str(e)}'}, 500


@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        """Login and get access & refresh tokens"""
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return {'message': 'Missing username or password'}, 400
        
        # Find user
        user = UserDAO.get_by_username(username)
        
        if not user or not user.check_password(password):
            return {'message': 'Invalid username or password'}, 401
        
        # Create both access and refresh tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        
        return {
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer',
            'expires_in': 1800,  # 30 minutes in seconds
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, 200


@auth_ns.route("/refresh")
class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """Get new access token using refresh token"""
        # Get user identity from refresh token
        user_id = get_jwt_identity()
        
        # Create new access token
        new_access_token = create_access_token(identity=str(user_id))

        
        return {
            'message': 'Token refreshed successfully',
            'access_token': new_access_token,
            'token_type': 'Bearer',
            'expires_in': 1800
        }, 200


@auth_ns.route("/me")
class CurrentUser(Resource):
    @jwt_required()
    def get(self):
        """Get current logged in user details"""
        user_id = get_jwt_identity()
        
        # Fetch user details
        from employee_app.models.user import User
        user = User.query.get(user_id)
        
        if not user:
            return {'message': 'User not found'}, 404
        
        return {
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at.isoformat() if user.created_at else None
            }
        }, 200


@auth_ns.route("/logout")
class Logout(Resource):
    @jwt_required()
    def post(self):
        """Logout (client should delete tokens)"""
        # Note: JWT tokens can't be invalidated on server-side without a blacklist
        # The client should delete the tokens from storage
        return {
            'message': 'Logout successful. Please delete your tokens on the client side.'
        }, 200



## **Step 3: How to Use Access & Refresh Tokens**

### **Workflow:**
# ```
# 1. User logs in
#    ↓
# 2. Server returns:
#    - access_token (expires in 30 mins)
#    - refresh_token (expires in 30 days)
#    ↓
# 3. User makes API requests with access_token
#    ↓
# 4. Access token expires after 30 mins
#    ↓
# 5. User sends refresh_token to /auth/refresh
#    ↓
# 6. Server returns new access_token
#    ↓
# 7. Repeat from step 3