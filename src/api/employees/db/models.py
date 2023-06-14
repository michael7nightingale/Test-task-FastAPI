from sqlalchemy import (Column, Integer, DateTime, String,
                        Boolean, ForeignKey, func)

from infrastructure.db import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(String(100), primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), unique=True)
    salary = Column(Integer)
    promotion_date = Column(DateTime(timezone=True))

    def as_dict(self) -> dict:
        return {i.name: getattr(self, i.name) for i in self.__table__.columns}
