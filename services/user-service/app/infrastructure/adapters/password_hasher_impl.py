from passlib.context import CryptContext

from app.application.interfaces.password_hasher_interface import PasswordHasherInterface

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordHasherImpl(PasswordHasherInterface):
    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
