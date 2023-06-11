from datetime import datetime
from abc import ABC, abstractmethod
from sqlalchemy import select
# import os, sys
# sys.path.append(os.getcwd())
from package.hasher import verify_password, hash_password
from package.auth import create_uuid
from database.init import Session
from database.models import Employee, User


class BaseManager(ABC):
    def __init__(self, session_class=Session):
        self.session_class = session_class

    @abstractmethod
    def all(self):
        pass

    @abstractmethod
    def create(self, *args, **kwargs):
        pass


class UserManager(BaseManager):
    async def login(self, username: str, password: str, *args, **kwargs) -> dict | None:
        async with self.session_class() as session:
            res = await session.execute(select(User).where(User.username == username))
            if res:
                user = res.first()[0]
                if verify_password(password, user.password):
                    return user.as_dict()

    async def create(self, username: str, email: str, password: str,
                       first_name: str, last_name: str, *args, **kwargs) -> dict:
        new_user = User(
            id=create_uuid(),
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=hash_password(password),
        )
        async with Session() as session:
            session.add(new_user)
            await session.commit()
        return new_user

    async def all(self):
        async with self.session_class() as session:
            res = await session.execute(select(User))
            return [i[0].as_dict() for i in res.all()]


class EmployeeManager(BaseManager):
    async def all(self) -> list[dict]:
        async with self.session_class() as session:
            res = await session.execute(select(Employee))
            return [i[0].as_dict() for i in res.all()]

    async def create(self, user_id: str, salary: int, promotion_date: datetime, *args, **kwargs):
        new_employee = Employee(
            id=create_uuid(),
            user_id=str(user_id),
            salary=salary,
            promotion_date=promotion_date
        )
        async with self.session_class() as session:
            session.add(new_employee)
            await session.commit()
        return new_employee

    async def get_by_userid(self, user_id: str):
        async with self.session_class() as session:
            res = await session.execute(select(Employee).where(Employee.user_id == user_id))
            if res:
                employee = res.first()[0]
                return employee


async def create_superuser(username: str = "admin",
                           password: str = 'password'):
    session = Session()
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
    async with Session() as session:
        session.add(superuser)
        await session.commit()
