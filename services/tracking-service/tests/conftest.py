import pytest
from src.app.application.interactors.action_interactors import CreateActionInteractor

from src.app.infrastructure.adapters.action_gateway import ActionGateway
from src.app.infrastructure.database.database import new_collection
from src.app.main.config import Config


@pytest.fixture
async def action_gateway():
    config = Config()
    collection = new_collection(
            config.mongodb,
            config.mongodb.db_name,
            config.mongodb.collection_name,
        )
    return ActionGateway(collection)


@pytest.fixture
async def action_interactor(action_gateway):
    return CreateActionInteractor(action_gateway)
        