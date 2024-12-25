import pytest

from app.application.interactors.user_interactors import (
    GetUserInteractor,
    UpdateUserInteractor,
)
from app.domain.entities.user_entity import UserDM


@pytest.mark.asyncio
async def test_get_user_interactor(mock_user_reader):
    # Подготовка
    email = "test@example.com"
    mock_user = UserDM(
        email=email, username="Test User", password="0123456789"
    )  # Замоканный объект UserDM
    mock_user_reader.read_by_email.return_value = mock_user

    # Интерактор
    interactor = GetUserInteractor(mock_user_reader)

    # Вызов
    result = await interactor(email)

    # Проверки
    mock_user_reader.read_by_email.assert_called_once_with(email)
    assert result == mock_user


@pytest.mark.asyncio
async def test_update_user_interactor(mock_user_updater):
    # Подготовка
    email = "test@example.com"
    update_data = {"name": "Updated User"}
    mock_user = UserDM(email=email, username="Updated User", password="0123456789")
    mock_user_updater.update.return_value = mock_user

    # Интерактор
    interactor = UpdateUserInteractor(mock_user_updater)

    # Вызов
    result = await interactor(email, update_data)

    # Проверки
    mock_user_updater.update.assert_called_once_with(email, update_data)
    assert result == mock_user
