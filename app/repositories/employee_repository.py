from ..models import Employee


class EmployeeRepository:

    def __init__(self, db):
        self.db = db

    def get_all(
        self,
        search=None,
        department=None
    ):

        query = self.db.query(Employee)

        if search:
            query = query.filter(
                Employee.name.ilike(
                    f"%{search}%"
                )
            )

        if department:
            query = query.filter(
                Employee.department == department
            )

        return query.order_by(
            Employee.id
        ).all()

    def get_by_id(self, employee_id):

        return (
            self.db.query(Employee)
            .filter(
                Employee.id == employee_id
            )
            .first()
        )

    def get_by_email(self, email):

        return (
            self.db.query(Employee)
            .filter(
                Employee.email == email
            )
            .first()
        )

    def create(self, employee):

        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)

        return employee

    def update(self, employee):

        self.db.commit()
        self.db.refresh(employee)

        return employee

    def delete(self, employee):

        self.db.delete(employee)
        self.db.commit()