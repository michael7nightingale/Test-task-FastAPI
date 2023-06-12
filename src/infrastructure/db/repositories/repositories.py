from sqlalchemy.orm import Session

from src.infrastructure.db.models.models import User, Employee
from src.infrastructure.db.repositories.base import BaseRepository
from src.schemas.user import UserShow, UserLogin, UserRegister
from src.schemas.employee import EmployeeShow, EmployeeInDb

from src.package.hasher import hash_password, verify_password


class UserRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(User, session)

    def create(self, user_schema: UserRegister):
        user = self._model(
            username=user_schema.username,
            password=hash_password(user_schema.password),
            email=user_schema.email,
            first_name=user_schema.first_name,
            last_name=user_schema.last_name
        )
        self.add(user)
        self.commit()
        return user

    def login(self, user_schema: UserLogin) -> User:
        user = self.filter(username=user_schema.username)
        if verify_password(user_schema.password, user.password):
            return user
        else:
            raise ValueError


class EmployeeRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Employee, session)

    def get_by_user_id(self, user_id) -> Employee:
        return self.filter(user_id=user_id)

    def create(self, employee_schema: EmployeeInDb) -> Employee:
        employee = self._model(
            user_id=employee_schema.user_id,
            salary=employee_schema.salary,
            promotion_date=employee_schema.promotion_date
        )
        self.add(employee)
        self.commit()
        return employee

