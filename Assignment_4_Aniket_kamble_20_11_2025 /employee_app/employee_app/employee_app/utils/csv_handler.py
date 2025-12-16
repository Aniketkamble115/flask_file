import csv
from io import StringIO
from datetime import datetime
# Make sure imports use employee_app prefix
from employee_app.models.employee import Employee  # if needed

def parse_employee_csv(file):
    """Parse uploaded CSV file and return list of employee dicts"""
    stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_reader = csv.DictReader(stream)
    rows = []
    for row in csv_reader:
        rows.append({
            'name': row['name'],
            'email': row['email'],
            'date_of_birth': datetime.strptime(row['date_of_birth'], '%Y-%m-%d').date(),
            'experience': float(row['experience']),
            'salary': float(row['salary'])
        })
    return rows

def generate_employee_csv(employees):
    """Generate CSV text from list of employee objects"""
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['id', 'name', 'email', 'date_of_birth', 'experience', 'salary'])
    for emp in employees:
        writer.writerow([emp.id, emp.name, emp.email, emp.date_of_birth, emp.experience, emp.salary])
    return output.getvalue()