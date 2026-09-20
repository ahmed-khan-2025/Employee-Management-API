def employee_data():
    return {
        "name": "Ahmed Khan",
        "email": "ahmed@example.com",
        "department": "IT",
        "salary": 55000,
    }


def test_create_employee(client, admin_token):
    response = client.post(
        "/employees/api",
        json=employee_data(),
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["name"] == "Ahmed Khan"
    assert data["email"] == "ahmed@example.com"
    assert data["department"] == "IT"
    assert float(data["salary"]) == 55000
    assert "id" in data


def test_create_employee_without_token(client):
    response = client.post(
        "/employees/api",
        json=employee_data(),
    )

    assert response.status_code == 401


def test_get_employees(client, admin_token):
    client.post(
        "/employees/api",
        json=employee_data(),
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    response = client.get(
        "/employees/api",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 1
    assert data[0]["name"] == "Ahmed Khan"


def test_get_employee_by_id(client, admin_token):
    create_response = client.post(
        "/employees/api",
        json=employee_data(),
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert create_response.status_code == 201

    employee_id = create_response.get_json()["id"]

    response = client.get(
        f"/employees/api/{employee_id}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == employee_id
    assert data["name"] == "Ahmed Khan"


def test_get_nonexistent_employee(client, admin_token):
    response = client.get(
        "/employees/api/999999",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert response.status_code == 404


def test_update_employee(client, admin_token):
    create_response = client.post(
        "/employees/api",
        json=employee_data(),
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert create_response.status_code == 201

    employee_id = create_response.get_json()["id"]

    updated_data = {
        "name": "Ahmed Updated",
        "email": "updated@example.com",
        "department": "Engineering",
        "salary": 65000,
    }

    response = client.put(
        f"/employees/api/{employee_id}",
        json=updated_data,
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["name"] == "Ahmed Updated"
    assert data["email"] == "updated@example.com"
    assert data["department"] == "Engineering"
    assert float(data["salary"]) == 65000


def test_update_employee_requires_role(client, user_token):
    response = client.put(
        "/employees/api/1",
        json=employee_data(),
        headers={
            "Authorization": f"Bearer {user_token}"
        },
    )

    assert response.status_code == 403


def test_manager_can_update_employee(
    client,
    admin_token,
    manager_token
):
    create_response = client.post(
        "/employees/api",
        json=employee_data(),
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert create_response.status_code == 201

    employee_id = create_response.get_json()["id"]

    response = client.put(
        f"/employees/api/{employee_id}",
        json={
            "name": "Updated By Manager",
            "email": "manager@example.com",
            "department": "IT",
            "salary": 60000,
        },
        headers={
            "Authorization": f"Bearer {manager_token}"
        },
    )

    assert response.status_code == 200


def test_delete_employee(client, admin_token):
    create_response = client.post(
        "/employees/api",
        json=employee_data(),
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert create_response.status_code == 201

    employee_id = create_response.get_json()["id"]

    response = client.delete(
        f"/employees/api/{employee_id}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    # Your DELETE API returns 200 OK
    assert response.status_code == 200

    # Confirm employee was actually deleted
    get_response = client.get(
        f"/employees/api/{employee_id}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert get_response.status_code == 404


def test_delete_employee_requires_admin(client, manager_token):
    response = client.delete(
        "/employees/api/1",
        headers={
            "Authorization": f"Bearer {manager_token}"
        },
    )

    assert response.status_code == 403


def test_delete_employee_requires_token(client):
    response = client.delete(
        "/employees/api/1"
    )

    assert response.status_code == 401


def test_duplicate_email(client, admin_token):
    data = employee_data()

    first = client.post(
        "/employees/api",
        json=data,
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert first.status_code == 201

    second = client.post(
        "/employees/api",
        json=data,
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert second.status_code == 409


def test_search_employee(client, admin_token):
    client.post(
        "/employees/api",
        json=employee_data(),
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    response = client.get(
        "/employees/api?search=Ahmed",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 1
    assert data[0]["name"] == "Ahmed Khan"


def test_department_filter(client, admin_token):
    client.post(
        "/employees/api",
        json=employee_data(),
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    response = client.get(
        "/employees/api?department=IT",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 1
    assert data[0]["department"] == "IT"