# Employee Management API

A production-style Employee Management System built with **Python, Flask, PostgreSQL, SQLAlchemy, Alembic, JWT authentication, Role-Based Access Control (RBAC), Swagger/OpenAPI, Repository-Service architecture, logging, health checks, and automated testing**.

The project provides both:

- REST API for employee management
- Web interface for managing employees
- JWT-based authentication
- Role-based authorization
- PostgreSQL database persistence
- Database migrations with Alembic
- Swagger API documentation
- Centralized logging and error handling
- Automated tests with pytest

---

# Features

## Employee Management

The application supports complete employee CRUD operations:

- Create employee
- List employees
- Get employee by ID
- Update employee
- Delete employee
- Search employees by name
- Filter employees by department
- Pagination
- Duplicate email validation

---

## Authentication

The application provides JWT-based authentication.

Supported operations:

- User registration
- User login
- Get current authenticated user
- Password hashing
- JWT access tokens
- Token expiration

Passwords are never stored as plain text.

Passwords are stored using Werkzeug password hashing.

---

## Role-Based Access Control

The application supports three roles:

| Role | Create | Read | Update | Delete |
|------|--------|------|--------|--------|
| Admin | Yes | Yes | Yes | Yes |
| Manager | Yes | Yes | Yes | No |
| User | No | Yes | No | No |

### Admin

Administrators have full access to employee management.

### Manager

Managers can:

- Create employees
- Read employees
- Update employees

Managers cannot delete employees.

### User

Normal users can only read employee information.

---

# Technology Stack

## Backend

- Python 3.14
- Flask
- SQLAlchemy
- Pydantic
- PostgreSQL
- psycopg2
- PyJWT
- Werkzeug

## API Documentation

- Flasgger
- Swagger UI
- OpenAPI

## Database Migration

- Alembic

## Testing

- pytest

## Configuration

- python-dotenv

## Logging

- Python logging
- Rotating file handler

---

# Project Architecture

The project follows a layered architecture.

```text
Client
   |
   v
Flask Routes / Blueprints
   |
   v
Authentication / Authorization
   |
   v
Service Layer
   |
   v
Repository Layer
   |
   v
SQLAlchemy
   |
   v
PostgreSQL
