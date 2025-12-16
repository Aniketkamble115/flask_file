from flask_restx import Namespace, Resource, fields
from flask import request, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from employee_app.providers.employee_provider import EmployeeProvider
from employee_app.schemas.employee_schema import EmployeeSchema
from employee_app.utils.csv_handler import parse_employee_csv, generate_employee_csv

# Namespace
employee_ns = Namespace("employees", description="Employee operations")

# Models for Swagger
employee_model = employee_ns.model('Employee', {
    'name': fields.String(required=True),
    'email': fields.String(required=True),
    'date_of_birth': fields.String(required=True, description='YYYY-MM-DD'),
    'experience': fields.Float(required=True),
    'salary': fields.Float(required=True),
})

# Schemas
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


# -------------------------
# Employee List / Create
# -------------------------
@employee_ns.route('')
class EmployeeList(Resource):
    def get(self):
        """List all employees"""
        include_deleted = request.args.get('include_deleted', 'false').lower() == 'true'
        employees = EmployeeProvider.list(include_deleted=include_deleted)
        return employees_schema.dump(employees)

    @employee_ns.expect(employee_model)
    @jwt_required()
    def post(self):
        """Create a new employee"""
        _ = str(get_jwt_identity())  # enforce string identity, even if unused
        data = request.get_json()
        emp = EmployeeProvider.create(data)
        return employee_schema.dump(emp), 201


# -------------------------
# Employee Detail / Update / Soft Delete
# -------------------------
@employee_ns.route('/<int:id>')
class EmployeeDetail(Resource):
    def get(self, id):
        """Get employee by ID"""
        emp = EmployeeProvider.get(id)
        if not emp:
            return {'message': 'Employee not found'}, 404
        return employee_schema.dump(emp)

    @jwt_required()
    def put(self, id):
        """Update employee by ID"""
        _ = str(get_jwt_identity())
        data = request.get_json()
        emp = EmployeeProvider.update(id, data)
        if not emp:
            return {'message': 'Employee not found'}, 404
        return employee_schema.dump(emp)

    @jwt_required()
    def delete(self, id):
        """Soft delete employee"""
        _ = str(get_jwt_identity())
        emp = EmployeeProvider.soft_delete(id)
        if not emp:
            return {'message': 'Employee not found'}, 404
        return {'message': 'Employee soft deleted'}


# -------------------------
# Hard Delete
# -------------------------
@employee_ns.route('/<int:id>/hard')
class EmployeeHardDelete(Resource):
    @jwt_required()
    def delete(self, id):
        """Hard delete employee permanently"""
        _ = str(get_jwt_identity())
        ok = EmployeeProvider.hard_delete(id)
        if not ok:
            return {'message': 'Employee not found'}, 404
        return {'message': 'Employee deleted permanently'}


# -------------------------
# CSV Upload
# -------------------------
@employee_ns.route('/upload')
class EmployeeUpload(Resource):
    @jwt_required()
    def post(self):
        """Upload employees from CSV"""
        _ = str(get_jwt_identity())
        if 'file' not in request.files:
            return {'message': 'No file uploaded'}, 400
        rows = parse_employee_csv(request.files['file'])
        created = []
        for r in rows:
            try:
                created.append(EmployeeProvider.create(r))
            except Exception:
                continue
        return employees_schema.dump(created), 201


# -------------------------
# CSV Download
# -------------------------
@employee_ns.route('/download')
class EmployeeDownload(Resource):
    def get(self):
        """Download all employees as CSV"""
        include_deleted = request.args.get('include_deleted', 'false').lower() == 'true'
        employees = EmployeeProvider.list(include_deleted=include_deleted)
        csv_text = generate_employee_csv(employees)
        return Response(
            csv_text,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=employees.csv'}
        )
