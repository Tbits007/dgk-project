from app.application.dtos.action_dtos import CreateActionDTO
from app.application.interactors.action_interactors import CreateActionInteractor
from app.infrastructure.broker import new_broker
from dishka.integrations.base import FromDishka
from dishka.integrations.faststream import inject

from app.main.config import Config
from app.presentation.controllers.schemas import ActionSchema 


actions = new_broker(
    kafka_config=Config().kafka,
)


@actions.subscriber("user-service-actions")
@inject 
async def handle_user_actions(
    data: ActionSchema,
    interactor: FromDishka[CreateActionInteractor]
    ) -> None:
    dto = CreateActionDTO(
        email=data.email,
        action_type=data.action_type,
        details=data.details,
        )
    await interactor(dto)
