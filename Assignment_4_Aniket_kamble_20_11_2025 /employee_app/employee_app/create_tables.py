import sys
import os

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from employee_app import create_app
from employee_app.extensions.db import db
from employee_app.models.user import User

app = create_app()

with app.app_context():
    db.create_all()
    print("Tables created successfully!")
