from ..models import User


class UserRepository:

    def __init__(self, db):
        self.db = db

    def get_by_id(self, user_id):

        return (
            self.db.query(User)
            .filter(
                User.id == user_id
            )
            .first()
        )

    def get_by_username(self, username):

        return (
            self.db.query(User)
            .filter(
                User.username == username
            )
            .first()
        )

    def create(self, user):

        self.db.add(user)

        self.db.commit()

        self.db.refresh(user)

        return user
