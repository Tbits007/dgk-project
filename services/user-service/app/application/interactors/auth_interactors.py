from app.application.dtos.user_dtos import CreateUserDTO, LoginUserDTO
from app.application.interfaces.email_sender_interface import EmailSender
from app.application.interfaces.jwt_processor_interface import (
    JwtProcessorInterface,
    TokenType,
)
from app.application.interfaces.password_hasher_interface import PasswordHasherInterface
from app.application.interfaces.user_interface import UserReader, UserSaver, UserUpdater
from app.domain.entities.user_entity import UserDM
from app.domain.exceptions.access import AuthenticationError


class RegisterInteractor:
    def __init__(
        self,
        user_gateway: UserSaver,
        email_gateway: EmailSender,
        jwt_token_processor: JwtProcessorInterface,
        password_hasher: PasswordHasherInterface,
    ) -> None:
        self._user_gateway = user_gateway
        self._email_gateway = email_gateway
        self._jwt_token_processor = jwt_token_processor
        self._password_hasher = password_hasher

    async def __call__(self, dto: CreateUserDTO) -> None:
        hashed_password = self._password_hasher.get_password_hash(dto.password)
        user = UserDM(
            email=dto.email,
            username=dto.username,
            password=hashed_password,
        )
        await self._user_gateway.save(user)
        token = self._jwt_token_processor.create_access_token(dto.email)
        verification_link = f"https://localhost:8000/verify-email?token={token}"
        await self._email_gateway.send_email(
            recipient=dto.email,
            subject="Account verification",
            body=f"Hi {dto.username}, visit the link: {verification_link} to verify account",
        )


class VerifyInteractor:
    def __init__(
        self, user_gateway: UserUpdater, jwt_token_processor: JwtProcessorInterface
    ) -> None:
        self._user_gateway = user_gateway
        self._jwt_token_processor = jwt_token_processor

    async def __call__(self, token: str) -> None:
        email = self._jwt_token_processor.verify_token(
            token, token_type=TokenType.ACCESS
        )
        await self._user_gateway.update(email, {"is_verified": True})


class LoginInteractor:
    def __init__(
        self,
        user_gateway: UserReader,
        password_hasher: PasswordHasherInterface,
        jwt_token_processor: JwtProcessorInterface,
    ) -> None:
        self._user_gateway = user_gateway
        self._password_hasher = password_hasher
        self._jwt_token_processor = jwt_token_processor

    async def __call__(self, dto: LoginUserDTO) -> dict:
        user = await self._user_gateway.read_by_email(dto.email)
        if not user or not self._password_hasher.verify_password(
            dto.password, user.password
        ):
            raise AuthenticationError
        if not user.is_verified:
            raise AuthenticationError

        access_token = self._jwt_token_processor.create_access_token(user.email)
        refresh_token = self._jwt_token_processor.create_refresh_token(user.email)
        return {"access_token": access_token, "refresh_token": refresh_token}


class PasswordResetInteractor:
    def __init__(
        self,
        user_gateway: UserReader,
        email_gateway: EmailSender,
        jwt_token_processor: JwtProcessorInterface,
    ) -> None:
        self._user_gateway = user_gateway
        self._email_gateway = email_gateway
        self._jwt_token_processor = jwt_token_processor

    async def __call__(self, email: str) -> None:
        user = await self._user_gateway.read_by_email(email)
        if user:
            token = self._jwt_token_processor.create_password_reset_token(email)
            reset_link = f"https://localhost:8000/reset-password?token={token}"
            await self._email_gateway.send_email(
                recipient=email,
                subject="Password Reset",
                body=f"Hi, visit the link: {reset_link} to reset your password.",
            )


class PasswordResetConfirmInteractor:
    def __init__(
        self,
        user_gateway: UserUpdater,
        password_hasher: PasswordHasherInterface,
        jwt_token_processor: JwtProcessorInterface,
    ):
        self._user_gateway = user_gateway
        self._password_hasher = password_hasher
        self._jwt_token_processor = jwt_token_processor

    async def __call__(self, token: str, password: str) -> None:
        email = self._jwt_token_processor.verify_token(
            token, token_type=TokenType.PASSWORD_RESET
        )
        hashed_password = self._password_hasher.get_password_hash(password)
        await self._user_gateway.update(email, {"password": hashed_password})
