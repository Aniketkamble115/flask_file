from extensions.bcrypt import bcrypt
from flask_jwt_extended import create_access_token
from models.user import User
from extensions.db import db

class AuthProvider:
    @staticmethod
    def register(data):
        user = User(name=data['name'], email=data['email'],
                    password=bcrypt.generate_password_hash(data['password']).decode())
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def login(user):
        return create_access_token(identity=str(user.id))

