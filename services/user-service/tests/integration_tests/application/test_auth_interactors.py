import pytest

from app.application.dtos.user_dtos import CreateUserDTO, LoginUserDTO
from app.application.interactors.auth_interactors import (
    LoginInteractor,
    PasswordResetConfirmInteractor,
    PasswordResetInteractor,
    RegisterInteractor,
    VerifyInteractor,
)
from app.application.interfaces.jwt_processor_interface import TokenType
from app.domain.entities.user_entity import UserDM


@pytest.mark.asyncio
async def test_register_interactor(
    mock_user_saver, mock_email_sender, mock_jwt_processor, mock_password_hasher
):
    # Подготовка
    # Входные данные
    dto = CreateUserDTO(
        email="test@example.com", username="TestUser", password="password123"
    )
    hashed_password = "hashed_password123"
    token = "test_token"
    verification_link = f"https://localhost:8000/verify-email?token={token}"

    # Настройка mock-объектов
    mock_password_hasher.get_password_hash.return_value = hashed_password
    mock_jwt_processor.create_access_token.return_value = token

    # Создание экземпляра интерактора
    interactor = RegisterInteractor(
        user_gateway=mock_user_saver,
        email_gateway=mock_email_sender,
        jwt_token_processor=mock_jwt_processor,
        password_hasher=mock_password_hasher,
    )

    # Вызов
    await interactor(dto)

    # Проверки
    # Проверка, что метод `save` был вызван с объектом UserDM
    mock_user_saver.save.assert_called_once_with(
        UserDM(email=dto.email, username=dto.username, password=hashed_password)
    )
    # Проверка, что `create_access_token` был вызван с правильным email
    mock_jwt_processor.create_access_token.assert_called_once_with(dto.email)
    # Проверка, что email был отправлен с правильным содержимым
    mock_email_sender.send_email.assert_called_once_with(
        recipient=dto.email,
        subject="Account verification",
        body=f"Hi {dto.username}, visit the link: {verification_link} to verify account",
    )


@pytest.mark.asyncio
async def test_verify_interactor(mock_user_updater, mock_jwt_processor):
    # Подготовка
    token = "test_token"
    email = "test@example.com"
    mock_jwt_processor.verify_token.return_value = email

    interactor = VerifyInteractor(
        user_gateway=mock_user_updater, jwt_token_processor=mock_jwt_processor
    )

    # Вызов
    await interactor(token)

    # Проверки
    mock_jwt_processor.verify_token.assert_called_once_with(
        token, token_type=TokenType.ACCESS
    )
    mock_user_updater.update.assert_called_once_with(email, {"is_verified": True})


@pytest.mark.asyncio
async def test_login_interactor(
    mock_user_reader, mock_password_hasher, mock_jwt_processor
):
    # Подготовка
    dto = LoginUserDTO(email="test@example.com", password="password123")
    user = UserDM(
        email=dto.email,
        username="TestUser",
        password="hashed_password",
        is_verified=True,
    )
    mock_user_reader.read_by_email.return_value = user
    mock_password_hasher.verify_password.return_value = True
    mock_jwt_processor.create_access_token.return_value = "access_token"
    mock_jwt_processor.create_refresh_token.return_value = "refresh_token"

    interactor = LoginInteractor(
        user_gateway=mock_user_reader,
        password_hasher=mock_password_hasher,
        jwt_token_processor=mock_jwt_processor,
    )

    # Вызов
    tokens = await interactor(dto)

    # Проверки
    mock_user_reader.read_by_email.assert_called_once_with(dto.email)
    mock_password_hasher.verify_password.assert_called_once_with(
        dto.password, user.password
    )
    assert tokens == {"access_token": "access_token", "refresh_token": "refresh_token"}


@pytest.mark.asyncio
async def test_password_reset_interactor(
    mock_user_reader, mock_email_sender, mock_jwt_processor
):
    # Подготовка
    email = "test@example.com"
    user = UserDM(email=email, username="TestUser", password="hashed_password")
    mock_user_reader.read_by_email.return_value = user
    mock_jwt_processor.create_password_reset_token.return_value = "reset_token"

    interactor = PasswordResetInteractor(
        user_gateway=mock_user_reader,
        email_gateway=mock_email_sender,
        jwt_token_processor=mock_jwt_processor,
    )

    # Вызов
    await interactor(email)

    # Проверки
    mock_user_reader.read_by_email.assert_called_once_with(email)
    mock_email_sender.send_email.assert_called_once_with(
        recipient=email,
        subject="Password Reset",
        body="Hi, visit the link: https://localhost:8000/reset-password?token=reset_token to reset your password.",
    )


@pytest.mark.asyncio
async def test_password_reset_confirm_interactor(
    mock_user_updater, mock_password_hasher, mock_jwt_processor
):
    # Подготовка
    token = "reset_token"
    new_password = "new_password123"
    hashed_password = "hashed_new_password"
    email = "test@example.com"
    mock_jwt_processor.verify_token.return_value = email
    mock_password_hasher.get_password_hash.return_value = hashed_password

    interactor = PasswordResetConfirmInteractor(
        user_gateway=mock_user_updater,
        password_hasher=mock_password_hasher,
        jwt_token_processor=mock_jwt_processor,
    )

    # Вызов
    await interactor(token, new_password)

    # Проверки
    mock_jwt_processor.verify_token.assert_called_once_with(
        token, token_type=TokenType.PASSWORD_RESET
    )
    mock_password_hasher.get_password_hash.assert_called_once_with(new_password)
    mock_user_updater.update.assert_called_once_with(
        email, {"password": hashed_password}
    )
