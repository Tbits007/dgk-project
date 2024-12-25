import pytest

from app.infrastructure.adapters.password_hasher_impl import PasswordHasherImpl


# Фикстура для инициализации PasswordHasherImpl
@pytest.fixture
def password_hasher():
    return PasswordHasherImpl()


# Тест на получение хэша пароля
def test_get_password_hash(password_hasher):
    password = "my_secure_password"

    # Получаем хэш пароля
    hashed_password = password_hasher.get_password_hash(password)

    # Проверяем, что хэш не равен исходному паролю
    assert hashed_password != password
    # Проверяем, что хэш является строкой
    assert isinstance(hashed_password, str)


# Тест на верификацию пароля
def test_verify_password(password_hasher):
    password = "my_secure_password"

    # Хэшируем пароль
    hashed_password = password_hasher.get_password_hash(password)

    # Проверяем корректный пароль
    assert password_hasher.verify_password(password, hashed_password) is True

    # Проверяем некорректный пароль
    wrong_password = "wrong_password"
    assert password_hasher.verify_password(wrong_password, hashed_password) is False


# Тест на проверку, что хэши одинаковых паролей различаются (случайные соли)
def test_hashes_are_unique(password_hasher):
    password = "my_secure_password"

    # Получаем два хэша для одного и того же пароля
    hashed_password1 = password_hasher.get_password_hash(password)
    hashed_password2 = password_hasher.get_password_hash(password)

    # Проверяем, что хэши не совпадают
    assert hashed_password1 != hashed_password2
