from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required
from providers.employee_provider import EmployeeProvider
from schemas import employee_schema
from marshmallow import ValidationError
from flasgger import swag_from
import io
from datetime import datetime

employee_bp = Blueprint("employees", __name__, url_prefix="/api/employees")


@employee_bp.route("", methods=["POST"])
@jwt_required()
def create_employee():
    try:
        data = employee_schema.load(request.json)
        result = EmployeeProvider.create_employee(data)
        return jsonify({"message": "Employee created successfully", "employee": result}), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@employee_bp.route("", methods=["GET"])
@jwt_required()
def get_all_employees():
    result = EmployeeProvider.get_all_employees()
    return jsonify(result), 200


@employee_bp.route("/<int:employee_id>", methods=["GET"])
@jwt_required()
def get_employee(employee_id):
    try:
        result = EmployeeProvider.get_employee_by_id(employee_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@employee_bp.route("/<int:employee_id>", methods=["PUT"])
@jwt_required()
def update_employee(employee_id):
    try:
        data = employee_schema.load(request.json, partial=True)
        result = EmployeeProvider.update_employee(employee_id, data)
        return jsonify({"message": "Employee updated successfully", "employee": result}), 200
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@employee_bp.route("/<int:employee_id>", methods=["DELETE"])
@jwt_required()
def soft_delete_employee(employee_id):
    try:
        result = EmployeeProvider.soft_delete_employee(employee_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@employee_bp.route("/<int:employee_id>/hard-delete", methods=["DELETE"])
@jwt_required()
def hard_delete_employee(employee_id):
    try:
        result = EmployeeProvider.hard_delete_employee(employee_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@employee_bp.route("/<int:employee_id>/restore", methods=["POST"])
@jwt_required()
def restore_employee(employee_id):
    try:
        result = EmployeeProvider.restore_employee(employee_id)
        return jsonify({"message": "Employee restored", "employee": result}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@employee_bp.route("/deleted", methods=["GET"])
@jwt_required()
def get_deleted_employees():
    result = EmployeeProvider.get_deleted_employees()
    return jsonify(result), 200


@employee_bp.route("/download", methods=["GET"])
@jwt_required()
def download_csv():
    employees = EmployeeProvider.get_all_employees()
    csv_output = EmployeeProvider.generate_csv(employees)

    return send_file(
        io.BytesIO(csv_output.getvalue().encode("utf-8")),
        mimetype="text/csv",
        as_attachment=True,
        download_name=f"employees_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )


@employee_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_csv():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.endswith(".csv"):
        return jsonify({"error": "File must be a CSV"}), 400

    try:
        result = EmployeeProvider.import_from_csv(file)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
