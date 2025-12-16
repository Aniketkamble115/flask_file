from employee_app.models.employee import Employee
from employee_app.extensions.db import db
from datetime import datetime

class EmployeeDAO:
    @staticmethod
    def list(include_deleted=False):
        query = Employee.query
        if not include_deleted:
            query = query.filter_by(is_deleted=False)
        return query.all()
    
    @staticmethod
    def get(emp_id):
        return Employee.query.filter_by(id=emp_id, is_deleted=False).first()
    
    @staticmethod
    def create(data):
        emp = Employee(**data)
        db.session.add(emp)
        db.session.commit()
        return emp
    
    @staticmethod
    def update(emp_id, data):
        emp = Employee.query.filter_by(id=emp_id, is_deleted=False).first()
        if not emp:
            return None
        for key, value in data.items():
            setattr(emp, key, value)
        db.session.commit()
        return emp
    
    @staticmethod
    def soft_delete(emp_id):
        emp = Employee.query.filter_by(id=emp_id, is_deleted=False).first()
        if not emp:
            return None
        emp.is_deleted = True
        emp.deleted_at = datetime.utcnow()
        db.session.commit()
        return emp
    
    @staticmethod
    def hard_delete(emp_id):
        emp = Employee.query.get(emp_id)
        if not emp:
            return False
        db.session.delete(emp)
        db.session.commit()
        return True