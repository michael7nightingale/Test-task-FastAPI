from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from uuid import uuid4

from package.utils import get_environ


SECRET_KEY = get_environ("SECRET_KEY")
EXPIRES_IN = 60 * 24
ALGORITHM = "HS256"
SCHEMES = ['bcrypt']
crypto_context = CryptContext(schemes=SCHEMES, deprecated='auto')


def decode_access_token(token) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return


def create_uuid():
    return str(uuid4())


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update(exp=datetime.utcnow() + timedelta(minutes=EXPIRES_IN))
    return jwt.encode(claims=data, key=SECRET_KEY, algorithm=ALGORITHM)

