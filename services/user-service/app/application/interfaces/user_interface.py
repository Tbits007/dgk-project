from abc import abstractmethod
from typing import Protocol

from app.domain.entities.user_entity import UserDM


class UserSaver(Protocol):
    @abstractmethod
    async def save(self, user: UserDM) -> None: ...


class UserReader(Protocol):
    @abstractmethod
    async def read_by_email(self, email: str) -> UserDM | None: ...


class UserUpdater(Protocol):
    @abstractmethod
    async def update(self, email: str, update_data: dict) -> UserDM | None: ...
