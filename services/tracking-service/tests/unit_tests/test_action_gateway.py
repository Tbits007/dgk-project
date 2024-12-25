import pytest
from src.app.domain.entities.action_entity import ActionDM


@pytest.mark.asyncio
async def test_save_action(action_gateway):
    """Тестирует сохранение действия."""
    action = ActionDM(
        email="test@mail.com", 
        action_type="test_action",
        details="test details",
    )
    saved_action = await action_gateway.save(action)

    # Проверяем, что сохранённый объект имеет ID
    assert saved_action is not None
    assert saved_action._id is not None
    assert saved_action.email == action.email
    assert saved_action.details == action.details


@pytest.mark.asyncio
async def test_read_by_id(action_gateway):
    """Тестирует чтение действия по ID."""
    # Создаём тестовые данные и добавляем их в коллекцию
    action = ActionDM(
        email="test@mail.com", 
        action_type="test_action",
        details="test details",
    )
    saved_action = await action_gateway.save(action)

    # Читаем объект через Gateway
    retrieved_action = await action_gateway.read_by_id(str(saved_action._id))

    # Проверяем, что данные корректно прочитаны
    assert retrieved_action is not None
    assert str(retrieved_action._id) == str(saved_action._id)
    assert retrieved_action.action_type == action.action_type
    assert retrieved_action.email == action.email
    assert retrieved_action.details == action.details