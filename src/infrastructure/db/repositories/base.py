from typing import TypeVar, Generic
from src.infrastructure.db.models.base import BaseAlchemyModel

from sqlalchemy.orm import Session
from sqlalchemy import delete, update, select

Model = TypeVar("Model", bound=BaseAlchemyModel)


class BaseRepository:
    def __init__(self, model: type[Model], session: Session):
        self._model = model
        self._session = session

    def get(self, id_: int) -> Model:
        query = select(self._model).where(self._model.id == id_)
        return self._session.execute(query).scalar_one_or_none()

    def filter(self, **kwargs) -> Model:
        query = select(self._model).filter_by(**kwargs)
        return self._session.execute(query).scalar_one_or_none()

    def all(self) -> list[Model]:
        query = select(self._model)
        return self._session.execute(query).scalars().all()

    def update(self, id_, **kwargs):
        query = update(self._model).where(self._model.id == id_).values(**kwargs)
        self._session.execute(query)

    def delete(self, id_) -> None:
        query = delete(self._model).where(self._model.id == id_)
        self._session.execute(query)
        self.commit()

    def commit(self):
        self._session.commit()

    def add(self, obj):
        self._session.add(obj)