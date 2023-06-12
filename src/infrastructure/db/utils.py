from src.infrastructure.db.models.models import User
from src.package.auth import create_uuid
from src.package.hasher import hash_password
from sqlalchemy.exc import IntegrityError


def create_superuser(pool):
    with pool() as session:
        try:
            superuser = User(
                id=create_uuid(),
                username='admin',
                password=hash_password('password'),
                first_name='Michael',
                last_name='Nightingale',
                email="suslanchikmopl@gmail.com",
                is_superuser=True,
                is_staff=True
            )

            session.add(superuser)
            session.commit()
        except IntegrityError:  # superuser exists
            pass

