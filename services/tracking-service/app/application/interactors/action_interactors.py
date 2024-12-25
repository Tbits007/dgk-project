from app.application.dtos.action_dtos import CreateActionDTO
from app.application.interfaces import action_interface
from app.domain.entities.action_entity import ActionDM


class GetActionInteractor:
    def __init__(
        self,
        action_gateway: action_interface.ActionReader,
    ) -> None:
        self._action_gateway = action_gateway

    async def __call__(self, _id: str) -> ActionDM | None:
        return await self._action_gateway.read_by_id(_id)


class CreateActionInteractor:
    def __init__(
        self,
        action_gateway: action_interface.ActionSaver,
    ) -> None:
        self._action_gateway = action_gateway

    async def __call__(self, dto: CreateActionDTO) -> ActionDM | None:
        action = ActionDM(
            email=dto.email,
            action_type=dto.action_type,
            details=dto.details, 
        )
        return await self._action_gateway.save(action)