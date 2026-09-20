from flask import (
    Blueprint,
    jsonify,
    request,
    render_template,
    redirect,
    url_for,
    flash
)

from ..database import get_db
from ..services.employee_service import EmployeeService
from ..schemas import (
    EmployeeCreate,
    EmployeeUpdate
)

from ..auth.security import (
    jwt_required,
    role_required,
    web_login_required
)


router = Blueprint(
    "employees",
    __name__
)


# =========================================================
# WEB ROUTES
# =========================================================


@router.get("/employees")
@web_login_required
def employees_page():

    db = get_db()

    try:

        search = request.args.get(
            "search",
            ""
        )

        department = request.args.get(
            "department",
            ""
        )

        page = request.args.get(
            "page",
            1,
            type=int
        )

        service = EmployeeService(db)

        employees = service.get_all(
            search=search,
            department=department
        )

        all_employees = service.get_all()

        departments = sorted(
            {
                employee.department
                for employee in all_employees
            }
        )

        per_page = 10

        total = len(employees)

        start = (
            page - 1
        ) * per_page

        end = start + per_page

        page_employees = employees[
            start:end
        ]

        pages = max(
            1,
            (total + per_page - 1)
            // per_page
        )

        pagination = {
            "page": page,
            "pages": pages,
            "has_prev": page > 1,
            "has_next": page < pages,
            "prev_num": page - 1,
            "next_num": page + 1
        }

        return render_template(
            "employees.html",
            employees=page_employees,
            search=search,
            department_filter=department,
            departments=departments,
            pagination=pagination
        )

    finally:

        db.close()


@router.get("/employees/create")
@web_login_required
def create_employee_page():

    return render_template(
        "employee_form.html",
        employee=None
    )


@router.post("/employees/create")
@web_login_required
def create_employee_web():

    db = get_db()

    try:

        data = {
            "name": request.form.get(
                "name",
                ""
            ).strip(),

            "email": request.form.get(
                "email",
                ""
            ).strip(),

            "department": request.form.get(
                "department",
                ""
            ).strip(),

            "salary": request.form.get(
                "salary",
                ""
            ).strip()
        }

        try:

            data["salary"] = float(
                data["salary"]
            )

            validated = (
                EmployeeCreate
                .model_validate(data)
            )

        except Exception as error:

            flash(
                str(error)
            )

            return render_template(
                "employee_form.html",
                employee=None
            )

        service = EmployeeService(db)

        try:

            service.create(
                validated.model_dump()
            )

        except ValueError as error:

            flash(
                str(error)
            )

            return render_template(
                "employee_form.html",
                employee=None
            )

        flash(
            "Employee created successfully."
        )

        return redirect(
            url_for(
                "employees.employees_page"
            )
        )

    finally:

        db.close()


@router.get("/employees/<int:employee_id>")
@web_login_required
def employee_detail(
    employee_id
):

    db = get_db()

    try:

        service = EmployeeService(db)

        employee = service.get_by_id(
            employee_id
        )

        if not employee:

            return (
                "Employee not found",
                404
            )

        return render_template(
            "employee_detail.html",
            employee=employee
        )

    finally:

        db.close()


@router.get(
    "/employees/<int:employee_id>/edit"
)
@web_login_required
def edit_employee_page(
    employee_id
):

    db = get_db()

    try:

        service = EmployeeService(db)

        employee = service.get_by_id(
            employee_id
        )

        if not employee:

            return (
                "Employee not found",
                404
            )

        return render_template(
            "employee_form.html",
            employee=employee
        )

    finally:

        db.close()


@router.post(
    "/employees/<int:employee_id>/edit"
)
@web_login_required
def update_employee_web(
    employee_id
):

    db = get_db()

    try:

        service = EmployeeService(db)

        employee = service.get_by_id(
            employee_id
        )

        if not employee:

            return (
                "Employee not found",
                404
            )

        data = {
            "name": request.form.get(
                "name",
                ""
            ).strip(),

            "email": request.form.get(
                "email",
                ""
            ).strip(),

            "department": request.form.get(
                "department",
                ""
            ).strip(),

            "salary": request.form.get(
                "salary",
                ""
            ).strip()
        }

        try:

            data["salary"] = float(
                data["salary"]
            )

            validated = (
                EmployeeUpdate
                .model_validate(data)
            )

        except Exception as error:

            flash(
                str(error)
            )

            return render_template(
                "employee_form.html",
                employee=employee
            )

        try:

            service.update(
                employee,
                validated.model_dump()
            )

        except ValueError as error:

            flash(
                str(error)
            )

            return render_template(
                "employee_form.html",
                employee=employee
            )

        flash(
            "Employee updated successfully."
        )

        return redirect(
            url_for(
                "employees.employee_detail",
                employee_id=employee.id
            )
        )

    finally:

        db.close()


@router.get(
    "/employees/<int:employee_id>/delete"
)
@web_login_required
def delete_employee_web(
    employee_id
):

    db = get_db()

    try:

        service = EmployeeService(db)

        employee = service.get_by_id(
            employee_id
        )

        if not employee:

            return (
                "Employee not found",
                404
            )

        service.delete(
            employee
        )

        flash(
            "Employee deleted successfully."
        )

        return redirect(
            url_for(
                "employees.employees_page"
            )
        )

    finally:

        db.close()


# =========================================================
# API - CREATE EMPLOYEE
# =========================================================


@router.post("/employees/api")
@role_required(
    "admin",
    "manager"
)
def create_employee_api():
    """
    Create a new employee
    ---
    tags:
      - Employees

    security:
      - Bearer: []

    consumes:
      - application/json

    parameters:
      - in: body
        name: employee
        required: true
        schema:
          type: object
          required:
            - name
            - email
            - department
            - salary
          properties:
            name:
              type: string
              example: John Smith
            email:
              type: string
              example: john@example.com
            department:
              type: string
              example: IT
            salary:
              type: number
              example: 55000

    responses:
      201:
        description: Employee created successfully

      400:
        description: Validation error

      401:
        description: Unauthorized

      403:
        description: Forbidden

      409:
        description: Email already exists
    """

    data = request.get_json(
        silent=True
    )

    if not data:

        return jsonify({
            "error": "Invalid request",
            "message": "JSON body is required"
        }), 400

    try:

        validated = (
            EmployeeCreate
            .model_validate(data)
        )

    except Exception as error:

        return jsonify({
            "error": "Validation error",
            "message": str(error)
        }), 400

    db = get_db()

    try:

        service = EmployeeService(db)

        try:

            employee = service.create(
                validated.model_dump()
            )

        except ValueError as error:

            return jsonify({
                "error": "Conflict",
                "message": str(error)
            }), 409

        return jsonify({
            "id": employee.id,
            "name": employee.name,
            "email": employee.email,
            "department": employee.department,
            "salary": employee.salary
        }), 201

    finally:

        db.close()


# =========================================================
# API - GET ALL EMPLOYEES
# =========================================================


@router.get("/employees/api")
@jwt_required()
def get_employees_api():
    """
    Get all employees
    ---
    tags:
      - Employees

    security:
      - Bearer: []

    responses:
      200:
        description: List of employees

      401:
        description: Unauthorized
    """

    db = get_db()

    try:

        service = EmployeeService(db)

        employees = service.get_all()

        return jsonify([
            {
                "id": employee.id,
                "name": employee.name,
                "email": employee.email,
                "department": employee.department,
                "salary": employee.salary
            }
            for employee in employees
        ])

    finally:

        db.close()


# =========================================================
# API - GET EMPLOYEE BY ID
# =========================================================


@router.get(
    "/employees/api/<int:employee_id>"
)
@jwt_required()
def get_employee_api(
    employee_id
):
    """
    Get employee by ID
    ---
    tags:
      - Employees

    security:
      - Bearer: []

    parameters:
      - in: path
        name: employee_id
        required: true
        type: integer
        example: 1

    responses:
      200:
        description: Employee found

      401:
        description: Unauthorized

      404:
        description: Employee not found
    """

    db = get_db()

    try:

        service = EmployeeService(db)

        employee = service.get_by_id(
            employee_id
        )

        if not employee:

            return jsonify({
                "error": "Not found",
                "message": "Employee not found"
            }), 404

        return jsonify({
            "id": employee.id,
            "name": employee.name,
            "email": employee.email,
            "department": employee.department,
            "salary": employee.salary
        })

    finally:

        db.close()


# =========================================================
# API - UPDATE EMPLOYEE
# =========================================================


@router.put(
    "/employees/api/<int:employee_id>"
)
@role_required(
    "admin",
    "manager"
)
def update_employee_api(
    employee_id
):
    """
    Update an employee
    ---
    tags:
      - Employees

    security:
      - Bearer: []

    consumes:
      - application/json

    parameters:
      - in: path
        name: employee_id
        required: true
        type: integer
        example: 1

      - in: body
        name: employee
        required: true
        schema:
          type: object
          required:
            - name
            - email
            - department
            - salary
          properties:
            name:
              type: string
              example: John Smith
            email:
              type: string
              example: john@example.com
            department:
              type: string
              example: IT
            salary:
              type: number
              example: 60000

    responses:
      200:
        description: Employee updated successfully

      400:
        description: Validation error

      401:
        description: Unauthorized

      403:
        description: Forbidden

      404:
        description: Employee not found

      409:
        description: Email already exists
    """

    data = request.get_json(
        silent=True
    )

    if not data:

        return jsonify({
            "error": "Invalid request",
            "message": "JSON body is required"
        }), 400

    try:

        validated = (
            EmployeeUpdate
            .model_validate(data)
        )

    except Exception as error:

        return jsonify({
            "error": "Validation error",
            "message": str(error)
        }), 400

    db = get_db()

    try:

        service = EmployeeService(db)

        employee = service.get_by_id(
            employee_id
        )

        if not employee:

            return jsonify({
                "error": "Not found",
                "message": "Employee not found"
            }), 404

        try:

            employee = service.update(
                employee,
                validated.model_dump()
            )

        except ValueError as error:

            return jsonify({
                "error": "Conflict",
                "message": str(error)
            }), 409

        return jsonify({
            "id": employee.id,
            "name": employee.name,
            "email": employee.email,
            "department": employee.department,
            "salary": employee.salary
        })

    finally:

        db.close()


# =========================================================
# API - DELETE EMPLOYEE
# =========================================================


@router.delete(
    "/employees/api/<int:employee_id>"
)
@role_required(
    "admin"
)
def delete_employee_api(
    employee_id
):
    """
    Delete an employee
    ---
    tags:
      - Employees

    security:
      - Bearer: []

    parameters:
      - in: path
        name: employee_id
        required: true
        type: integer
        example: 1

    responses:
      200:
        description: Employee deleted successfully

      401:
        description: Unauthorized

      403:
        description: Forbidden

      404:
        description: Employee not found
    """

    db = get_db()

    try:

        service = EmployeeService(db)

        employee = service.get_by_id(
            employee_id
        )

        if not employee:

            return jsonify({
                "error": "Not found",
                "message": "Employee not found"
            }), 404

        service.delete(
            employee
        )

        return jsonify({
            "message": "Employee deleted successfully"
        })

    finally:

        db.close()