from dao.employee_dao import EmployeeDAO
from schemas import employee_schema, employees_schema
from marshmallow import ValidationError
import csv
import io


class EmployeeProvider:
    """
    Provider Layer - Business Logic
    """

    @staticmethod
    def create_employee(data):
        existing = EmployeeDAO.get_employee_by_email(data['email'])
        if existing:
            raise ValueError("Employee with this email already exists")

        employee = EmployeeDAO.create_employee(data)
        return employee_schema.dump(employee)

    @staticmethod
    def get_all_employees():
        employees = EmployeeDAO.get_all_employees()
        return employees_schema.dump(employees)

    @staticmethod
    def get_employee_by_id(employee_id):
        employee = EmployeeDAO.get_employee_by_id(employee_id)
        if not employee:
            raise ValueError("Employee not found")
        return employee_schema.dump(employee)

    @staticmethod
    def update_employee(employee_id, data):

        if 'email' in data:
            existing = EmployeeDAO.get_employee_by_email(data['email'])
            if existing and existing.id != employee_id:
                raise ValueError("Email already in use by another employee")

        employee = EmployeeDAO.update_employee(employee_id, data)
        if not employee:
            raise ValueError("Employee not found")

        return employee_schema.dump(employee)

    @staticmethod
    def soft_delete_employee(employee_id):
        employee = EmployeeDAO.soft_delete_employee(employee_id)
        if not employee:
            raise ValueError("Employee not found")
        return {"message": "Employee deleted successfully"}

    @staticmethod
    def hard_delete_employee(employee_id):
        success = EmployeeDAO.hard_delete_employee(employee_id)
        if not success:
            raise ValueError("Employee not found")
        return {"message": "Employee permanently deleted"}

    @staticmethod
    def restore_employee(employee_id):
        employee = EmployeeDAO.restore_employee(employee_id)
        if not employee:
            raise ValueError("Employee not found in deleted list")
        return employee_schema.dump(employee)

    @staticmethod
    def get_deleted_employees():
        employees = EmployeeDAO.get_deleted_employees()
        return employees_schema.dump(employees)

    @staticmethod
    def generate_csv(employees_data):
        output = io.StringIO()
        writer = csv.writer(output)

        # 🔥 MAKE HEADERS MATCH CSV IMPORT
        writer.writerow(['id', 'name', 'email', 'date_of_birth', 'experience', 'salary', 'created_at'])

        for emp in employees_data:
            writer.writerow([
                emp['id'],
                emp['name'],
                emp['email'],
                emp['date_of_birth'],
                emp['experience'],
                emp['salary'],
                emp['created_at']
            ])

        output.seek(0)
        return output

    @staticmethod
    def import_from_csv(file):
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.DictReader(stream)

        added_count = 0
        errors = []

        from datetime import datetime

        for row_num, row in enumerate(csv_reader, start=2):

            try:
                employee_data = {
                    'name': row.get('name', '').strip(),
                    'email': row.get('email', '').strip(),
                    'date_of_birth': datetime.strptime(row.get('date_of_birth'), '%Y-%m-%d').date(),
                    'experience': int(row.get('experience')),
                    'salary': float(row.get('salary'))
                }

                employee_schema.load(employee_data)

                if EmployeeDAO.get_employee_by_email(employee_data['email']):
                    errors.append(f"Row {row_num}: Email {employee_data['email']} already exists")
                    continue

                EmployeeDAO.create_employee(employee_data)
                added_count += 1

            except Exception as e:
                errors.append(f"Row {row_num}: {str(e)}")

        return {
            "message": f"Successfully added {added_count} employees",
            "errors": errors or None
        }
