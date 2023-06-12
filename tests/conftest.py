import pytest
import asyncio
from fastapi.testclient import TestClient
import os, sys
sys.path.append("\\".join(os.getcwd().split('\\')[:-1]))

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker

from src.config import (DB_NAME_TEST, DB_USER_TEST, DB_HOST_TEST, DB_PASSWORD_TEST, DB_PORT_TEST)
from src.main import app
from src.database.init import Base
from src.database.managers import UserManager, create_superuser


test_engine: Engine = create_engine(
    url=f"postgresql://{DB_USER_TEST}:{DB_PASSWORD_TEST}@{DB_HOST_TEST}/{DB_NAME_TEST}"
)
TestSession = sessionmaker(bind=test_engine)


def create_test_db():
    Base.metadata.bind = test_engine
    # Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    create_superuser(session_class=TestSession)
    yield
    # Base.metadata.drop_all(bind=test_engine)


client = TestClient(app)


# um = UserManager(session_class=TestSession)



