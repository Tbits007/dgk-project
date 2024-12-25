import pytest
from src.app.presentation.controllers.schemas import ActionSchema
from src.app.presentation.controllers.handlers import handle_user_actions


@pytest.mark.asyncio
async def test_handle_user_actions(action_interactor):
    """Тестируем обработку сообщений в хендлере."""
    # Подготавливаем тестовые данные
    test_data = ActionSchema(
        email="test@example.com",
        action_type="TEST_ACTION",
        details="Test details",
    )
    # Вызываем хендлер
    result = await handle_user_actions(
        data=test_data,
        interactor=action_interactor
    )
    assert result is None