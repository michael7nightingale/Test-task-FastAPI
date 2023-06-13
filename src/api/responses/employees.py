from enum import Enum


class EmployeesDetail(Enum):
    employee_not_found = "Employee with such data is not found."
    employee_create_error = "Employee cannot be created. Data is invalid"
    not_authenticated = "You are not authenticated."
    no_permissions = "You do not have permissions to access this data about employees."


