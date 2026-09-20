from ..models import Employee
from ..repositories.employee_repository import (
    EmployeeRepository
)


class EmployeeService:

    def __init__(self, db):

        self.repository = EmployeeRepository(db)

    def get_all(
        self,
        search=None,
        department=None
    ):

        return self.repository.get_all(
            search=search,
            department=department
        )

    def get_by_id(self, employee_id):

        return self.repository.get_by_id(
            employee_id
        )

    def create(self, data):

        existing = self.repository.get_by_email(
            data["email"]
        )

        if existing:

            raise ValueError(
                "Email already exists"
            )

        employee = Employee(
            name=data["name"],
            email=data["email"],
            department=data["department"],
            salary=data["salary"]
        )

        return self.repository.create(
            employee
        )

    def update(self, employee, data):

        existing = self.repository.get_by_email(
            data["email"]
        )

        if (
            existing
            and existing.id != employee.id
        ):
            raise ValueError(
                "Email already exists"
            )

        employee.name = data["name"]
        employee.email = data["email"]
        employee.department = data["department"]
        employee.salary = data["salary"]

        return self.repository.update(
            employee
        )

    def delete(self, employee):

        self.repository.delete(
            employee
        )