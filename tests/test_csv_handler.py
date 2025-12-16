import io
import os
import sys
import importlib.util
from types import SimpleNamespace
import pytest

# Load the csv_handler module directly from its file so we don't import the full
# package (which pulls in optional dependencies like flask_restx not needed here).
csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'employee_app', 'employee_app', 'utils', 'csv_handler.py'))
spec = importlib.util.spec_from_file_location('csv_handler', csv_path)
csv_mod = importlib.util.module_from_spec(spec)

# Provide a minimal dummy `employee_app.models.employee.Employee` so the
# csv_handler import doesn't try to import the real package (which requires
# Flask-related dependencies). The real Employee class isn't needed for our
# unit tests of parsing/generating CSV texts.
import types
pkg = types.ModuleType('employee_app')
models_pkg = types.ModuleType('employee_app.models')
emp_mod = types.ModuleType('employee_app.models.employee')
class Employee:
    pass
emp_mod.Employee = Employee
sys.modules['employee_app'] = pkg
sys.modules['employee_app.models'] = models_pkg
sys.modules['employee_app.models.employee'] = emp_mod

spec.loader.exec_module(csv_mod)

parse_employee_csv = csv_mod.parse_employee_csv
generate_employee_csv = csv_mod.generate_employee_csv


@pytest.fixture
def sample_csv_bytes():
    csv_text = (
        "name,email,date_of_birth,experience,salary\n"
        "Alice,alice@example.com,1990-05-01,5,55000\n"
        "Bob,bob@example.com,1985-10-12,10,75000\n"
    )
    return csv_text.encode("utf-8")


@pytest.fixture
def uploaded_file(sample_csv_bytes):
    # Emulate an uploaded file object with a .stream.read() method
    class Uploaded:
        def __init__(self, b):
            self.stream = io.BytesIO(b)

    return Uploaded(sample_csv_bytes)


def test_parse_employee_csv_basic(uploaded_file):
    rows = parse_employee_csv(uploaded_file)
    assert isinstance(rows, list)
    assert len(rows) == 2
    alice = rows[0]
    assert alice["name"] == "Alice"
    assert alice["email"] == "alice@example.com"
    assert str(alice["date_of_birth"]) == "1990-05-01"
    assert isinstance(alice["experience"], float)
    assert alice["experience"] == 5.0
    assert alice["salary"] == 55000.0


def test_parse_employee_csv_missing_field():
    # CSV missing the 'email' column should raise a KeyError when accessed
    csv_text = "name,date_of_birth,experience,salary\nJohn,1992-01-01,3,40000\n"
    uploaded = SimpleNamespace(stream=io.BytesIO(csv_text.encode("utf-8")))
    with pytest.raises(KeyError):
        parse_employee_csv(uploaded)


def test_parse_employee_csv_invalid_date():
    # Invalid date format should raise a ValueError from datetime.strptime
    csv_text = "name,email,date_of_birth,experience,salary\nJack,jack@example.com,01-01-1992,3,40000\n"
    uploaded = SimpleNamespace(stream=io.BytesIO(csv_text.encode("utf-8")))
    with pytest.raises(ValueError):
        parse_employee_csv(uploaded)


@pytest.fixture
def simple_employees():
    # Create lightweight objects with attributes used by generate_employee_csv
    e1 = SimpleNamespace(id=1, name="Alice", email="alice@example.com", date_of_birth="1990-05-01", experience=5.0, salary=55000.0)
    e2 = SimpleNamespace(id=2, name="Bob", email="bob@example.com", date_of_birth="1985-10-12", experience=10.0, salary=75000.0)
    return [e1, e2]


def test_generate_employee_csv_basic(simple_employees):
    csv_out = generate_employee_csv(simple_employees)
    # header + two rows -> 3 lines
    lines = [line for line in csv_out.splitlines() if line.strip() != ""]
    assert lines[0].startswith("id,name,email,date_of_birth,experience,salary")
    assert "Alice" in lines[1]
    assert "Bob" in lines[2]


def test_generate_employee_csv_empty():
    csv_out = generate_employee_csv([])
    # Should still include header
    assert csv_out.strip().startswith("id,name,email,date_of_birth,experience,salary")
