import os
from dotenv import load_dotenv
load_dotenv()


def get_environ(key: str) -> str:
    """Function to get a value from env or raise an exception."""
    value = os.environ.get(key)
    if value is None:
        raise KeyError(f"Missing required environ variable from the key: {key}")
    return value


# Development database variables
DB_NAME = get_environ('DB_NAME')
DB_HOST = get_environ("DB_HOST")
DB_PORT = get_environ("DB_PORT")
DB_USER = get_environ("DB_USER")
DB_PASSWORD = get_environ("DB_PASSWORD")

# Test database variables
DB_NAME_TEST = get_environ('DB_NAME_TEST')
DB_HOST_TEST = get_environ("DB_HOST_TEST")
DB_PORT_TEST = get_environ("DB_PORT_TEST")
DB_USER_TEST = get_environ("DB_USER_TEST")
DB_PASSWORD_TEST = get_environ("DB_PASSWORD_TEST")

# Auth variables
EXPIRE_MINUTES = 60 * 24
ALGORITHM = "HS256"
SECRET_KEY = get_environ("SECRET_KEY")
