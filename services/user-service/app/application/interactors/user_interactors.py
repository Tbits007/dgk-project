from app.application.interfaces import user_interface
from app.domain.entities.user_entity import UserDM


class GetUserInteractor:
    def __init__(
        self,
        user_gateway: user_interface.UserReader,
    ) -> None:
        self._user_gateway = user_gateway

    async def __call__(self, email: str) -> UserDM | None:
        return await self._user_gateway.read_by_email(email)


class UpdateUserInteractor:
    def __init__(
        self,
        user_gateway: user_interface.UserUpdater,
    ) -> None:
        self._user_gateway = user_gateway

    async def __call__(self, email: str, update_data: dict) -> UserDM | None:
        return await self._user_gateway.update(email, update_data)
