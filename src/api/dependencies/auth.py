from fastapi import Depends, Body
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette.exceptions import HTTPException

from src.infrastructure.db.repositories.repositories import UserRepository
from src.api.dependencies.database import get_repository
from src.package.auth import decode_access_token
from src.schemas.user import UserLogin, UserShow


oauth_scheme = OAuth2PasswordBearer(tokenUrl="auth/token/")


async def get_current_user(token: str = Depends(oauth_scheme)) -> UserShow:
    """Dependency for getting user from token"""
    user_data = decode_access_token(token)
    return UserShow(**user_data)


async def login_current_user(user_repo: UserRepository = Depends(get_repository(UserRepository)),
                             user_form: UserLogin = Body()):    # OAuth2PasswordRequestForm if needed
    """Dependency for getting user by login data from DB."""
    try:
        user = user_repo.login(user_form)
        return user
    except AttributeError:
        raise HTTPException(status_code=403, detail="Login data is not valid")


async def get_superuser(user: UserShow = Depends(get_current_user)):
    """Checks if current user is superuser"""
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="No permissions to watch this data.")
    return user
