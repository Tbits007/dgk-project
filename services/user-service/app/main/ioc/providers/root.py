from typing import AsyncGenerator

from dishka import Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.application.interfaces.email_sender_interface import EmailSender
from app.infrastructure.adapters.email_sender_impl import EmailSenderImpl
from app.infrastructure.database.database import new_session_maker
from app.main.config import Config


class RootProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncGenerator[AsyncSession, None]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.APP)
    def email_sender(self, config: Config) -> EmailSender:
        return EmailSenderImpl(
            smtp_server=config.smtp.host,
            smtp_port=config.smtp.port,
            username=config.smtp.login,
            password=config.smtp.password,
        )
