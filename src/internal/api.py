from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError, PendingRollbackError

from package.auth import decode_access_token, create_access_token
from package.schemas import UserShow, User, UserInDb, EmployeeInDb, Employee
from database.dao import UserDAO, EmployeeDAO
from database.init import Session


main_router = APIRouter(prefix='')
auth_router = APIRouter(prefix='/auth', tags=['Auth'])
employee_router = APIRouter(prefix='/employees', tags=['Employee'])

oauth_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


# ============================== DEPENDENCIES ============================== #

async def get_session():
    with Session() as ses:
        yield ses


async def get_current_user(token: str = Depends(oauth_scheme)) -> UserShow:
    """Dependency for getting user from token"""
    user_data = decode_access_token(token)
    return UserShow(**user_data)


async def login_current_user(session: Session = Depends(get_session), user_form: OAuth2PasswordRequestForm = Depends()):
    """Dependency for getting user by login data from DB."""
    try:
        user = UserDAO.login(session, username=user_form.username, password=user_form.password)
        return user
    except AttributeError:
        raise HTTPException(status_code=403, detail="Login data is not valid")


# ================================= ENDPOINTS ============================== #

@main_router.get("/", tags=["Homepage"])
async def root():
    """Home page"""
    return {"message": "If you see the message, service is working!"}


@auth_router.post("/register")
async def register_user(session: Session = Depends(get_session),
                        ser: UserInDb = Body()) -> UserShow:
    """Register user endpoint. All schema data is needed."""
    data = user.dict()
    registered_user = UserDAO.create(session, **data)
    return UserShow(**registered_user)


@auth_router.post("/token")
async def get_token(user_data: dict = Depends(login_current_user)):
    """Get auth token by login data (username, password) in request Body"""
    to_encode = UserShow(**user_data).dict()
    token = create_access_token(to_encode)
    return {"access_token": token}


@main_router.get("/users/all", tags=['Users'])
async def users_list(session: Session = Depends(get_session),
                     user: UserShow = Depends(get_current_user)) -> list[dict]:
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail='No permissions')
    users: list[dict] = UserDAO.all(session)
    return users


@employee_router.get("/all")
async def employees_list(session: Session = Depends(get_session),
                         user: UserShow = Depends(get_current_user)) -> list[dict]:
    """Shows all employees to superuser."""
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail='No permissions')

    employees = EmployeeDAO.all(session)
    return employees


@employee_router.post('/create')
async def create_employee(session: Session = Depends(get_session),
                          user: UserShow = Depends(get_current_user),
                          employee: EmployeeInDb = Body()) -> dict:
    """Superuser can create an employee, if three are some users."""
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail='No permissions')
    try:
        employee: dict = EmployeeDAO.create(session, **employee.dict())
        return employee
    except (IntegrityError, PendingRollbackError):  # foreign key does not exist
        raise HTTPException(status_code=402, detail="User does not exists.")


@employee_router.get('/me')
async def get_employee(session: Session = Depends(get_session),
                       user: UserShow = Depends(get_current_user)):
    """Get current employee from token-user"""
    try:
        employee = EmployeeDAO.get_by_userid(session, user.id)
        return Employee(**employee).dict()
    except AttributeError:     # employee of current user does not exist
        raise HTTPException(status_code=404, detail="Employee with such as user_id is not found")


