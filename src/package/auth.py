from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from uuid import uuid4

from config import EXPIRE_MINUTES, SECRET_KEY, ALGORITHM


crypto_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def decode_access_token(token) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return


def create_uuid():
    return str(uuid4())


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update(exp=datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES))
    return jwt.encode(claims=data, key=SECRET_KEY, algorithm=ALGORITHM)

