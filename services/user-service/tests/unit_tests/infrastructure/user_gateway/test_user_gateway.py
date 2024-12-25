import pytest
from sqlalchemy import select

from app.domain.entities.user_entity import UserDM
from app.infrastructure.adapters.user_gateway import UserGateway
from tests.unit_tests.infrastructure.user_gateway.models.user_model import User


# Тест на сохранение пользователя
@pytest.mark.asyncio
async def test_save_user(setup_database, async_session):
    user_gateway = UserGateway(async_session)
    user_dm = UserDM(
        email="test@example.com",
        username="testuser",
        password="hashed_password",
        is_active=True,
        is_verified=False,
        is_superuser=False,
    )
    await user_gateway.save(user_dm)

    # Проверяем, что пользователь появился в базе данных
    result = await async_session.execute(
        select(User).where(User.email == "test@example.com")
    )
    user = result.scalar_one_or_none()

    assert user is not None
    assert user.email == user_dm.email
    assert user.username == user_dm.username


# Тест на чтение пользователя по email
@pytest.mark.asyncio
async def test_read_user_by_email(setup_database, async_session):
    user_gateway = UserGateway(async_session)
    # Добавляем пользователя напрямую в базу
    user = User(
        email="test@example.com",
        username="testuser",
        password="hashed_password",
        is_active=True,
        is_verified=False,
        is_superuser=False,
    )
    async_session.add(user)
    await async_session.commit()

    # Читаем пользователя через gateway
    user_dm = await user_gateway.read_by_email("test@example.com")

    assert user_dm is not None
    assert user_dm.email == "test@example.com"
    assert user_dm.username == "testuser"


# Тест на обновление пользователя
@pytest.mark.asyncio
async def test_update_user(setup_database, async_session):
    user_gateway = UserGateway(async_session)
    # Добавляем пользователя напрямую в базу
    user = User(
        email="test@example.com",
        username="testuser",
        password="hashed_password",
        is_active=True,
        is_verified=False,
        is_superuser=False,
    )
    async_session.add(user)
    await async_session.commit()

    # Обновляем пользователя
    update_data = {"username": "updateduser", "is_verified": True}
    updated_user_dm = await user_gateway.update("test@example.com", update_data)
    await async_session.refresh(user)
    # Проверяем обновление
    assert updated_user_dm is not None
    assert updated_user_dm.username == "updateduser"
    assert updated_user_dm.is_verified is True

    # Проверяем изменения в базе
    result = await async_session.execute(
        select(User).where(User.email == "test@example.com")
    )
    updated_user = result.scalar_one()
    assert updated_user.username == "updateduser"
    assert updated_user.is_verified is True


# Тест на обновление несуществующего пользователя
@pytest.mark.asyncio
async def test_update_nonexistent_user(setup_database, async_session):
    user_gateway = UserGateway(async_session)
    with pytest.raises(ValueError) as exc_info:
        await user_gateway.update(
            "nonexistent@example.com", {"username": "updateduser"}
        )
    assert "not found" in str(exc_info.value)
