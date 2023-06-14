
from .models import User
from infrastructure.repository.base import BaseRepository

from infrastructure.utils.auth import create_uuid
from infrastructure.utils.hasher import verify_password, hash_password
from ..schemas import UserLogin, UserRegister

from sqlalchemy.orm import Session


class UserRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(User, session)

    def create(self, user_schema: UserRegister):
        user = self._model(
            id=create_uuid(),
            username=user_schema.username,
            password=hash_password(user_schema.password),
            email=user_schema.email,
            first_name=user_schema.first_name,
            last_name=user_schema.last_name
        )
        self.add(user)
        self.commit()
        return user

    def login_oauth(self, username: str, password: str) -> User:
        user = self.filter(username=username)
        if verify_password(password, user.password):
            return user
        else:
            raise ValueError

    def login(self, user_schema: UserLogin) -> User:
        user = self.filter(username=user_schema.username)
        if verify_password(user_schema.password, user.password):
            return user
        else:
            raise ValueError
