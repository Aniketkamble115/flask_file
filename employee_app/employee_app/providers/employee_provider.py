from employee_app.dao.employee_dao import EmployeeDAO

class EmployeeProvider:
    @staticmethod
    def list(include_deleted=False):
        return EmployeeDAO.list(include_deleted)
    
    @staticmethod
    def get(emp_id):
        return EmployeeDAO.get(emp_id)
    
    @staticmethod
    def create(data):
        return EmployeeDAO.create(data)
    
    @staticmethod
    def update(emp_id, data):
        return EmployeeDAO.update(emp_id, data)
    
    @staticmethod
    def soft_delete(emp_id):
        return EmployeeDAO.soft_delete(emp_id)
    
    @staticmethod
    def hard_delete(emp_id):
        return EmployeeDAO.hard_delete(emp_id)