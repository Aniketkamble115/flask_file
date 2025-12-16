from employee_app.extensions.db import db
from datetime import datetime

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)  # Add index
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)  # Add index
    date_of_birth = db.Column(db.Date, nullable=False)
    experience = db.Column(db.Float, nullable=False)
    salary = db.Column(db.Float, nullable=False)
    
    # Soft delete fields
    is_deleted = db.Column(db.Boolean, default=False, index=True)  # Add index
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Employee {self.name}>'