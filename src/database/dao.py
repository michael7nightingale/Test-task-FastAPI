from datetime import datetime
from abc import ABC, abstractmethod
from typing import Type
from sqlalchemy.orm import Session

from package.hasher import verify_password, hash_password
from package.auth import create_uuid
from database.init import Session
from database.models import Employee, User


class BaseDAO(ABC):
    model = None

    @classmethod
    @abstractmethod
    def all(cls, session):
        pass

    @classmethod
    @abstractmethod
    def create(cls, session, *args, **kwargs):
        pass


class UserDAO(BaseDAO):
    model = User

    @classmethod
    def login(cls, session, username: str, password: str, *args, **kwargs) -> dict:
        user = session.query(cls.model).filter_by(username=username).first()
        if verify_password(password, user.password):
            return user.as_dict()
        else:
            raise ValueError

    @classmethod
    def create(cls, session, username: str, email: str, password: str,
               first_name: str, last_name: str, *args, **kwargs) -> dict:
        new_user = cls.model(
            id=create_uuid(),
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=hash_password(password),
        )
        session.add(new_user)
        session.flush()
        session.commit()
        return new_user.as_dict()

    @classmethod
    def all(cls, session):
        users = session.query(cls.model).all()
        return [inst.as_dict() for inst in users]


class EmployeeDAO(BaseDAO):
    model = Employee

    @classmethod
    def all(cls, session) -> list[dict]:
        users = session.query(cls.model).all()
        return [inst.as_dict() for inst in users]

    @classmethod
    def create(cls, session, user_id: str, salary: int,
               promotion_date: datetime, *args, **kwargs) -> dict:
        new_employee = cls.model(
            id=create_uuid(),
            user_id=str(user_id),
            salary=salary,
            promotion_date=promotion_date
        )
        session.add(new_employee)
        session.flush()
        session.commit()
        return new_employee.as_dict()

    @classmethod
    def get_by_userid(cls, session, user_id: str) -> dict:
        employee = session.query(cls.model).filter_by(user_id=user_id).first()
        return employee.as_dict()


def create_superuser(username: str = "admin",
                     password: str = 'password',
                     session: Session = Session()):
    superuser = User(
        id=create_uuid(),
        username=username,
        first_name='Michael',
        last_name="Nightingale",
        email="suslanchikmopl@gmail.com",
        password=hash_password(password),
        is_superuser=True,
        is_staff=True
    )
    session.add(superuser)
    session.commit()
