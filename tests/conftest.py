import pytest

from app.main import app
from app.database import Base, engine, SessionLocal
from app.models import User


@pytest.fixture
def flask_app():

    app.config.update(
        TESTING=True,
        SECRET_KEY="test-secret-key-for-employee-management-2026",
        JWT_SECRET_KEY="test-jwt-secret-key-for-employee-management-2026",
    )

    # Create tables
    Base.metadata.create_all(bind=engine)

    yield app

    # Remove all test data/tables
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(flask_app):
    return flask_app.test_client()


@pytest.fixture
def db(flask_app):

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------
# USERS
# ---------------------------------------------------------

@pytest.fixture
def admin_user(db):

    user = User(
        username="admin",
        role="admin",
    )

    user.set_password("admin123")

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@pytest.fixture
def manager_user(db):

    user = User(
        username="manager",
        role="manager",
    )

    user.set_password("manager123")

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@pytest.fixture
def normal_user(db):

    user = User(
        username="user1",
        role="user",
    )

    user.set_password("user123")

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# ---------------------------------------------------------
# JWT TOKENS
# ---------------------------------------------------------

@pytest.fixture
def admin_token(client, admin_user):

    response = client.post(
        "/auth/login",
        json={
            "username": "admin",
            "password": "admin123",
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "access_token" in data

    return data["access_token"]


@pytest.fixture
def manager_token(client, manager_user):

    response = client.post(
        "/auth/login",
        json={
            "username": "manager",
            "password": "manager123",
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "access_token" in data

    return data["access_token"]


@pytest.fixture
def user_token(client, normal_user):

    response = client.post(
        "/auth/login",
        json={
            "username": "user1",
            "password": "user123",
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "access_token" in data

    return data["access_token"]