from abc import abstractmethod
from typing import Protocol

from app.domain.entities.action_entity import ActionDM


class ActionSaver(Protocol):
    @abstractmethod
    async def save(self, action: ActionDM) -> ActionDM | None:
        """Сохранить действие в базе данных."""
        ...


class ActionReader(Protocol):
    @abstractmethod
    async def read_by_id(self, _id: str) -> ActionDM | None:
        """Получить действие по _id."""
        ...
        