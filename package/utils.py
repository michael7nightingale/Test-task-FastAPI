import os


def get_environ(key: str) -> str:
    value = os.environ.get(key)
    if value is None:
        raise KeyError(f"Missing required environ variable from the key: {key}")
    return value
