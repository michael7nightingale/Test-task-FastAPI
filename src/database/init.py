from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, declarative_base

import os, sys
sys.path.append(os.getcwd() + "\\src\\")

from config import (DB_NAME, DB_USER, DB_HOST, DB_PASSWORD, DB_PORT)


engine: Engine = create_engine(
        url=f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)

Session = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()

