from marshmallow import Schema, fields, validate

class EmployeeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    date_of_birth = fields.Date(required=True)
    experience = fields.Int(required=True, validate=validate.Range(min=0, max=50))
    salary = fields.Float(required=True, validate=validate.Range(min=0))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    is_deleted = fields.Bool(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True)

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)
