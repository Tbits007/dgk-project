from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.user_interface import UserReader, UserSaver, UserUpdater
from app.domain.entities.user_entity import UserDM
from app.infrastructure.database.models.user_model import User


class UserGateway(UserReader, UserSaver, UserUpdater):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, user: UserDM) -> None:
        """Сохраняет нового пользователя в базе данных."""
        db_user = User(
            email=user.email,
            username=user.username,
            password=user.password,
            is_active=user.is_active,
            is_verified=user.is_verified,
            is_superuser=user.is_superuser,
        )
        self._session.add(db_user)
        await self._session.commit()

    async def read_by_email(self, email: str) -> UserDM | None:
        """Читает пользователя из базы данных по email."""
        query = select(User).where(User.email == email)
        result = await self._session.execute(query)
        try:
            db_user = result.scalar_one()
            return UserDM(
                email=db_user.email,
                username=db_user.username,
                password=db_user.password,
                is_active=db_user.is_active,
                is_verified=db_user.is_verified,
                is_superuser=db_user.is_superuser,
            )
        except Exception:
            return None

    async def update(self, email: str, update_data: dict) -> UserDM | None:
        """Обновляет данные пользователя в базе данных."""
        query = select(User).where(User.email == email)
        result = await self._session.execute(query)
        try:
            db_user = result.scalar_one()
            for field, value in update_data.items():
                if hasattr(db_user, field):
                    setattr(db_user, field, value)
            await self._session.commit()

            # Преобразуем ORM-модель в доменную модель
            return UserDM(
                email=db_user.email,
                username=db_user.username,
                password=db_user.password,
                is_active=db_user.is_active,
                is_verified=db_user.is_verified,
                is_superuser=db_user.is_superuser,
            )
        except Exception as e:
            await self._session.rollback()
            raise ValueError(f"User with email {email} not found") from e
