# dao/employee_dao.py
from extensions import db
from models.user_model import Employee
from datetime import datetime

class EmployeeDAO:
    @staticmethod
    def create_employee(data):
        emp = Employee(
            name=data['name'],
            email=data['email'],
            date_of_birth=data['date_of_birth'],
            experience=data['experience'],
            salary=data['salary']
        )
        db.session.add(emp)
        db.session.commit()
        return emp

    @staticmethod
    def get_all_employees(include_deleted=False):
        if include_deleted:
            return Employee.query.all()
        return Employee.query.filter_by(is_deleted=False).all()

    @staticmethod
    def get_employee_by_id(employee_id, include_deleted=False):
        emp = Employee.query.get(employee_id)
        if emp and (include_deleted or not emp.is_deleted):
            return emp
        return None

    @staticmethod
    def get_employee_by_email(email, include_deleted=False):
        if include_deleted:
            return Employee.query.filter_by(email=email).first()
        return Employee.query.filter_by(email=email, is_deleted=False).first()

    @staticmethod
    def update_employee(employee_id, data):
        emp = EmployeeDAO.get_employee_by_id(employee_id)
        if not emp:
            return None
        for k, v in data.items():
            setattr(emp, k, v)
        emp.updated_at = datetime.utcnow()
        db.session.commit()
        return emp

    @staticmethod
    def soft_delete_employee(employee_id):
        emp = EmployeeDAO.get_employee_by_id(employee_id)
        if not emp:
            return None
        emp.is_deleted = True
        emp.deleted_at = datetime.utcnow()
        db.session.commit()
        return emp

    @staticmethod
    def hard_delete_employee(employee_id):
        emp = EmployeeDAO.get_employee_by_id(employee_id, include_deleted=True)
        if not emp:
            return False
        db.session.delete(emp)
        db.session.commit()
        return True

    @staticmethod
    def restore_employee(employee_id):
        emp = Employee.query.get(employee_id)
        if not emp or not emp.is_deleted:
            return None
        emp.is_deleted = False
        emp.deleted_at = None
        db.session.commit()
        return emp

    @staticmethod
    def get_deleted_employees():
        return Employee.query.filter_by(is_deleted=True).all()
