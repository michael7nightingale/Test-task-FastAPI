from fastapi import APIRouter, Depends, Body
from starlette.exceptions import HTTPException

from sqlalchemy.exc import IntegrityError, PendingRollbackError

from src.api.dependencies.database import get_repository
from src.api.dependencies.auth import get_current_user, get_superuser
from src.infrastructure.db.repositories.repositories import EmployeeRepository
from src.infrastructure.db.models.models import Employee

from src.schemas.user import UserShow
from src.schemas.employee import EmployeeInDb, EmployeeShow


employees_router = APIRouter(prefix='/employees', tags=["Employees"])


@employees_router.get("/all")
async def employees_list(employee_repo: EmployeeRepository = Depends(get_repository(EmployeeRepository)),
                         superuser: UserShow = Depends(get_superuser)):
    """Shows all employees to superuser."""
    employees: list[Employee] = employee_repo.all()
    return [e.as_dict() for e in employees]


@employees_router.post('/create', response_model=EmployeeShow)
async def create_employee(employee_repo: EmployeeRepository = Depends(get_repository(EmployeeRepository)),
                          superuser: UserShow = Depends(get_superuser),
                          employee_schema: EmployeeInDb = Body()):
    """Superuser can create an employee, if three are some users."""
    try:
        employee: Employee = employee_repo.create(employee_schema=employee_schema)
        return employee.as_dict()
    except (IntegrityError, PendingRollbackError):  # foreign key does not exist
        raise HTTPException(status_code=402, detail="User does not exists.")


@employees_router.get('/me', response_model=EmployeeShow)
async def get_employee(employee_repo: EmployeeRepository = Depends(get_repository(EmployeeRepository)),
                       user: UserShow = Depends(get_current_user)):
    """Get current employee from token-user"""
    try:
        employee: Employee = employee_repo.filter(user_id=user.id)
        return employee.as_dict()
    except (AttributeError, TypeError):     # employee of current user does not exist
        raise HTTPException(status_code=404, detail="Employee with such as user_id is not found")