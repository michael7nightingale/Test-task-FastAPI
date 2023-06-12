import json

import pytest
import os, sys
sys.path.append(os.getcwd())

from conftest import client, app, TestSession
from src.database.managers import UserManager


class TestHttp:
    def test_homepage(self):
        response = client.get(app.url_path_for('root'))
        assert response.status_code == 200

    def test_register(self):
        # user_data = {
        #     "username": "postgres2007",
        #     "password": "psw102938",
        #     "first_name": "Oplasm",
        #     "last_name": None,
        #     "email": "sql@gmail.com"
        # }
        # response = client.post(
        #     url=app.url_path_for('register_user'),
        #     data=json.dumps(user_data)
        # )
        um = UserManager(TestSession)
        assert um.all() == []

    def test_users_list_get_no_permissions(self):
        response = client.get(app.url_path_for("users_list"))
        assert response.status_code == 401

    def test_employees_list_get_no_permissions(self):
        response = client.get(app.url_path_for("employees_list"))
        assert response.status_code == 401

    def test_employee_create_no_permissions(self):
        response = client.post(app.url_path_for('create_employee'))
        assert response.status_code == 401

    def test_employee_get_no_auth(self):
        response = client.get(app.url_path_for('get_employee'))
        assert response.status_code == 401
