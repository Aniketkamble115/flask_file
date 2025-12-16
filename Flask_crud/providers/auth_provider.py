from dao.user_dao import UserDAO
from flask_jwt_extended import create_access_token


class AuthProvider:
    """
    Authentication Provider
    Handles user registration and login logic
    """

    @staticmethod
    def register_user(data):
        """Register a new user"""

        # Validate email
        if UserDAO.get_user_by_email(data['email']):
            raise ValueError("Email already registered")

        # Validate username
        if UserDAO.get_user_by_username(data['username']):
            raise ValueError("Username already taken")

        # Create user
        UserDAO.create_user(data)
        return {"message": "User registered successfully"}

    @staticmethod
    def login_user(data):
        """Login user and generate JWT token"""

        user = UserDAO.get_user_by_email(data['email'])

        if not user or not user.check_password(data['password']):
            raise ValueError("Invalid email or password")

        # Generate JWT token
        access_token = create_access_token(identity=str(user.id))

        return {
            "message": "Login successful",
            "access_token": access_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }
