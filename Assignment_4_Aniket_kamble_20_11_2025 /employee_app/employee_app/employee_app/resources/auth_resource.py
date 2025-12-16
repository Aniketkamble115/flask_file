from flask_restx import Namespace, Resource
from schemas.user_schema import UserSchema
from providers.auth_provider import AuthProvider
from models.user import User
from extensions.bcrypt import bcrypt

api = Namespace("auth")

user_schema = UserSchema()

@api.route("/register")
class Register(Resource):
    def post(self):
        return {"message": "register endpoint"}

@api.route("/login")
class Login(Resource):
    def post(self):
        return {"message": "login endpoint"}
