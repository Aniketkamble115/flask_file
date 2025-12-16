from marshmallow import Schema, fields

class EmployeeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    date_of_birth = fields.Date(required=True)
    experience = fields.Float(required=True)
    salary = fields.Float(required=True)
    is_deleted = fields.Bool(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)