from enum import Enum


class AuthDetail(Enum):
    user_not_found = "User with such data is not found."
    not_authenticated = "You are not authenticated."
    login_data_error = "Login data is invalid."
    no_permissions = "You do not have permissions to access this data about users."


