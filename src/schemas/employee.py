from pydantic import BaseModel, Field
from pydantic.types import UUID4
from datetime import datetime


class EmployeeShow(BaseModel):
    """Schema for getting employee data"""
    salary: int = Field(gt=0)
    promotion_date: datetime


class EmployeeInDb(EmployeeShow):
    user_id: UUID4
