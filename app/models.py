from datetime import datetime, timezone

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from sqlalchemy import (
    Integer,
    String,
    DateTime
)

from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Employee(Base):

    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    department: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    salary: Mapped[float] = mapped_column(
        nullable=False
    )


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="user"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(
            password
        )

    def check_password(self, password: str) -> bool:
        return check_password_hash(
            self.password_hash,
            password
        )

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(
            password
        )

    def check_password(self, password: str) -> bool:
        return check_password_hash(
            self.password_hash,
            password
        )