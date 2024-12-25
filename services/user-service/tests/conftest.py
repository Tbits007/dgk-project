import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from tests.config import get_postgres_config
from tests.unit_tests.infrastructure.user_gateway.models.base_model import Base


@pytest.fixture
async def engine():
    engine = create_async_engine(get_postgres_config().DATABASE_URL, pool_recycle=1800)
    return engine


# Фикстура для создания базы данных
@pytest.fixture
async def setup_database(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def new_session_maker(engine):
    return async_sessionmaker(
        engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
    )


@pytest.fixture
async def async_session(new_session_maker):
    async with new_session_maker() as session:
        yield session
