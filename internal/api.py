from fastapi import APIRouter, Body, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette.exceptions import HTTPException
from fastapi.exceptions import ValidationError, RequestValidationError
from sqlalchemy.exc import IntegrityError, PendingRollbackError

from package.auth import decode_access_token, create_access_token
from package.schemas import UserShow, User, UserInDb, EmployeeInDb, Employee
from package.database import Session, UserManager, EmployeeManager


main_router = APIRouter(prefix='')
auth_router = APIRouter(prefix='/auth', tags=['Auth'])
employee_router = APIRouter(prefix='/employees', tags=['Employee'])
oauth_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


# session = Session()
user_manager = UserManager()
employee_manager = EmployeeManager()


@main_router.get("/", tags=["Homepage"])
async def root():
    """Home page"""
    return {"message": "If you see the message, service is working!"}


@auth_router.post("/register")
async def register_user(user: UserInDb = Body()) -> UserShow:
    """Register user endpoint. All schema data is needed."""
    data = user.dict()
    registered_user = await user_manager.create(**data)
    return UserShow(**data)


async def login_current_user(user_form: OAuth2PasswordRequestForm = Depends()):
    """Dependency for getting user by login data from DB."""
    try:
        user = await user_manager.login(username=user_form.username, password=user_form.password)
        return user
    except:
        raise HTTPException(status_code=403, detail="Login data is not valid")


@auth_router.post("/token")
async def get_token(user_data: dict = Depends(login_current_user)):
    to_encode = UserShow(**user_data).dict()
    token = create_access_token(to_encode)
    return {"access_token": token}


async def get_current_user(token: str = Depends(oauth_scheme)):
    user_data = decode_access_token(token)
    return UserShow(**user_data)


@main_router.get("/users-list", tags=['Users'])
async def users_list(user: UserShow = Depends(get_current_user)):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail='No permissions')
    users = await user_manager.all()
    return users


@employee_router.get("/employees-list")
async def employees_list(user: UserShow = Depends(get_current_user)):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail='No permissions')

    employees = await employee_manager.all()
    return employees


@employee_router.post('/create')
async def create_employee(user: UserShow = Depends(get_current_user),
                          employee: EmployeeInDb = Body()):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail='No permissions')
    try:
        employee = await employee_manager.create(**employee.dict())
        # return employee.as_dict()
        return {"id": employee.id,
                "user_id": employee.user_id,
                "salary": employee.salary,
                "promotion_date": employee.promotion_date}
    except (IntegrityError, PendingRollbackError):  # foreign key does not exist
        raise HTTPException(status_code=402, detail="User does not exists.")


@employee_router.get('/me')
async def get_employee(user: UserShow = Depends(get_current_user)):
    try:
        employee = await employee_manager.get_by_userid(user.id)
        return Employee(**employee.as_dict()).dict()
    except:     # no result
        return HTTPException(status_code=404, detail="Employee with such as user_id is not found")


