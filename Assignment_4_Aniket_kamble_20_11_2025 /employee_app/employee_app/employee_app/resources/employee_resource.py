from flask_restx import Namespace, Resource

api = Namespace("employee")

@api.route("/")
class EmpList(Resource):
    def get(self):
        return {"message": "employee list"}
