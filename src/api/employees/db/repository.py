from .models import Employee
from infrastructure.repository.base import BaseRepository

from infrastructure.utils.auth import create_uuid
from ..schemas import EmployeeInDb

from sqlalchemy.orm import Session


class EmployeeRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Employee, session)

    def get_by_user_id(self, user_id) -> Employee:
        return self.filter(user_id=user_id)

    def create(self, employee_schema: EmployeeInDb) -> Employee:
        print(employee_schema)
        employee = self._model(
            id=create_uuid(),
            user_id=str(employee_schema.user_id),
            salary=employee_schema.salary,
            promotion_date=employee_schema.promotion_date
        )
        self.add(employee)
        self.commit()
        return employee
