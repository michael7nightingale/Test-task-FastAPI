from sqlalchemy.orm import Session
from sqlalchemy import delete

from src.infrastructure.db.models.models import User, Employee
from src.infrastructure.db.repositories.base import BaseRepository
from src.schemas.user import UserShow, UserLogin, UserRegister
from src.schemas.employee import EmployeeShow, EmployeeInDb

from src.package.hasher import hash_password, verify_password
from src.package.auth import create_uuid


class UserRepository(BaseRepository):
    """
    Repository for User model
    """
    def __init__(self, session: Session):
        super().__init__(User, session)   # note: model is prescribed

    def create(self, user_schema: UserRegister):
        """Register method"""
        user_schema.password = hash_password(user_schema.password)
        new_user = super().create(**user_schema.dict())
        return new_user

    def login(self, user_schema: UserLogin) -> User:
        user = self.filter(username=user_schema.username)
        if verify_password(user_schema.password, user.password):
            return user
        else:
            raise ValueError


class EmployeeRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Employee, session)  # note: model is prescribed

    def get_by_user_id(self, user_id) -> Employee:
        return self.filter(user_id=user_id)

    def create(self, employee_schema: EmployeeInDb) -> Employee:
        """Create employee view"""
        new_employee = super().create(**employee_schema.dict())
        return new_employee

