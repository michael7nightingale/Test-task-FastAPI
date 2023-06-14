from api.auth.db.models import User
from infrastructure.utils.auth import create_uuid
from infrastructure.utils.hasher import hash_password
from sqlalchemy.exc import IntegrityError

from config import get_app_settings


def create_superuser(pool):
    with pool() as session:
        settings = get_app_settings()
        try:
            superuser = User(
                id=create_uuid(),
                username=settings.SUPERUSER_NAME,
                password=hash_password(settings.SUPERUSER_PASSWORD),
                first_name='Michael',
                last_name='Nightingale',
                email=settings.SUPERUSER_EMAIL,
                is_superuser=True,
                is_staff=True
            )

            session.add(superuser)
            session.commit()
        except IntegrityError:  # superuser exists
            pass

