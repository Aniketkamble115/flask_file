from extensions.db import db
from models.user_model import User


class UserDAO:
    """
    Data Access Object Layer for User
    Handles all database operations for User authentication
    """

    @staticmethod
    def create_user(data):
        """Create a new user"""
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_all_users():
        """Get all users"""
        return User.query.all()

    @staticmethod
    def get_user_by_email(email):
        """Get user by email"""
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_username(username):
        """Get user by username"""
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        return User.query.get(user_id)

    @staticmethod
    def update_user(user_id, data):
        """Update user details"""
        user = UserDAO.get_user_by_id(user_id)
        if not user:
            return None

        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.set_password(data['password'])

        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        """Delete user permanently"""
        user = UserDAO.get_user_by_id(user_id)
        if not user:
            return False

        db.session.delete(user)
        db.session.commit()
        return True
