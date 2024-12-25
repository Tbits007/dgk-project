import motor
from app.infrastructure.database.database import new_collection
from app.main.config import Config, KafkaConfig
from dishka import Provider, Scope, from_context, provide


class RootProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)
    
    @provide(scope=Scope.APP)
    def get_collection(
        self,
        config: Config
    ) -> motor.motor_asyncio.AsyncIOMotorCollection:
        
        return new_collection(
            config.mongodb,
            config.mongodb.db_name,
            config.mongodb.collection_name,
        )
    
