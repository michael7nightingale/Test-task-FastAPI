from sqlalchemy import (Column, Integer, DateTime, String,
                        Boolean, ForeignKey, func, Table)

from src.infrastructure.db import Base


class TableMixin:
    """For getting dict object of the model."""
    __table__: Table

    def as_dict(self):
        return {i.name: getattr(self, i.name) for i in self.__table__.columns}


class User(Base, TableMixin):
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


class Employee(Base, TableMixin):
    __tablename__ = "employees"

    id = Column(String(100), primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), unique=True)
    salary = Column(Integer)
    promotion_date = Column(DateTime(timezone=True))
