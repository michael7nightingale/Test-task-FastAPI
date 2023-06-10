import pytest
from fastapi.testclient import TestClient
import json


from conftest import client, app, drop_db, create_db, engine
import asyncio
from src.package.database import UserManager

# asyncio.run(drop_db(engine))
# asyncio.run(create_db(engine))
um = UserManager()

res = asyncio.run(um.all())
print(res)


def setUp():
    data = {"username": "michael7nightingale",
            "email": "python@mail.ru",
            'first_name': "Mick",
            "last_name": "Jagger",
            "password": "rammqueen123",
            "is_superuser": True}
    # print(json.dumps(data))
    response = client.post(
        url=app.url_path_for("register_user"),
        content=json.dumps(data),
        headers={}

    )
    return json.loads(response.text)

# print(setUp())


def test_homepage():
    response = client.get(app.url_path_for('root'))
    user = setUp()
    assert user["username"] == 'michael7nightingale'
    assert response.status_code == 200


def test_employees_list():
    response = client.get(app.url_path_for("employees_list"))
    assert response.status_code == 401

