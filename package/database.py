from datetime import datetime
from abc import ABC, abstractmethod
from sqlalchemy import MetaData, Column, Integer, DateTime, String, Boolean, ForeignKey, select
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_session, AsyncSession, AsyncEngine
import asyncio
from dotenv import load_dotenv
load_dotenv()

from package.utils import get_environ
from package.hasher import verify_password, hash_password
from package.auth import create_uuid


DB_NAME = get_environ('DB_NAME')
DB_HOST = get_environ("DB_HOST")
DB_PORT = get_environ("DB_PORT")
DB_USER = get_environ("DB_USER")
DB_PASSWORD = get_environ("DB_PASSWORD")


engine: AsyncEngine = create_async_engine(
    url=f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)
metadata = MetaData()
Session = sessionmaker(bind=engine, class_=AsyncSession, autocommit=False, autoflush=True)
Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = 'users'

    id = Column(String(100), primary_key=True)
    username = Column(String(40), unique=True)
    first_name = Column(String(40))
    last_name = Column(String(40), nullable=True)
    email = Column(String(50), unique=True)
    password = Column(String(200))
    last_login = Column(DateTime(timezone=True), server_default=func.now())
    date_join = Column(DateTime(timezone=True), server_default=func.now())
    is_superuser = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)

    def as_dict(self) -> dict:
        return {i.name: getattr(self, i.name) for i in self.__table__.columns}


class Employee(Base):
    __tablename__ = "employees"

    id = Column(String(100), primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), unique=True)
    salary = Column(Integer)
    promotion_date = Column(DateTime(timezone=True))

    def as_dict(self) -> dict:
        return {i.name: getattr(self, i.name) for i in self.__table__.columns}


class BaseManager(ABC):
    def __init__(self):
        # self._session = session
        ...

    # @property
    # def session(self):
    #     return self._session

    @abstractmethod
    def all(self):
        pass

    @abstractmethod
    def create(self, *args, **kwargs):
        pass


class UserManager(BaseManager):
    async def login(self, username: str, password: str, *args, **kwargs) -> dict | None:
        async with Session() as session:
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
        async with Session() as session:
            res = await session.execute(select(User))
            return [i[0].as_dict() for i in res.all()]


class EmployeeManager(BaseManager):
    async def all(self) -> list[dict]:
        async with Session() as session:
            res = await session.execute(select(Employee))
            return [i[0].as_dict() for i in res.all()]

    async def create(self, user_id: str, salary: int, promotion_date: datetime, *args, **kwargs):
        new_employee = Employee(
            id=create_uuid(),
            user_id=str(user_id),
            salary=salary,
            promotion_date=promotion_date
        )
        async with Session() as session:
            session.add(new_employee)
            await session.commit()
        return new_employee

    async def get_by_userid(self, user_id: str):
        async with Session() as session:
            res = await session.execute(select(Employee).where(Employee.user_id == user_id))
            if res:
                employee = res.first()[0]
                return employee



async def create_db():
    """Create tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    """Drop tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


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


if __name__ == '__main__':
    # asyncio.run(create_db())
    # asyncio.run(drop_db())
    # asyncio.run(create_superuser())
    ...



