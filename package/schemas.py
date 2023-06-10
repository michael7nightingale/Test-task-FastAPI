from pydantic import BaseModel, Field
from pydantic.types import UUID4
from datetime import datetime


class User(BaseModel):
    """Schema for logging"""
    username: str = Field(min_length=5, max_length=40)
    password: str = Field(min_length=5, max_length=40)


class UserInDb(User):
    """Schema for registering"""
    email: str = Field(min_length=5, max_length=50)
    first_name: str
    last_name: str | None = None


class UserShow(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str | None = None
    is_superuser: bool


class Employee(BaseModel):
    """Schema for getting employee data"""
    salary: int = Field(gt=0)
    promotion_date: datetime


class EmployeeInDb(Employee):
    user_id: UUID4
