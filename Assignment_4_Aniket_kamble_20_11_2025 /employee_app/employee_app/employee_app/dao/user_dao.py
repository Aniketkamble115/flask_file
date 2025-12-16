from employee_app.models.user import User
from employee_app.extensions.db import db

class UserDAO:
    @staticmethod
    def create(username, email, password):
        """Create a new user"""
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def get_by_username(username):
        """Find user by username"""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_by_email(email):
        """Find user by email"""
        return User.query.filter_by(email=email).first()