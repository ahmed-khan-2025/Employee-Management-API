from ..models import User
from ..repositories.user_repository import UserRepository
from ..auth.security import create_access_token


class AuthService:

    def __init__(self, db):

        self.repository = UserRepository(db)

    def register(
        self,
        username,
        password
    ):

        existing_user = (
            self.repository
            .get_by_username(username)
        )

        if existing_user:

            raise ValueError(
                "Username already exists"
            )

        user = User(
            username=username,
            role="user"
        )

        user.set_password(
            password
        )

        return self.repository.create(
            user
        )

    def authenticate(
        self,
        username,
        password
    ):

        user = (
            self.repository
            .get_by_username(username)
        )

        if (
            not user
            or not user.check_password(password)
        ):

            raise ValueError(
                "Invalid username or password"
            )

        token = create_access_token(
            user.id,
            user.username,
            user.role
        )

        return user, token
