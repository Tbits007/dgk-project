import motor.motor_asyncio

from app.main.config import MongoDBConfig


def new_collection(
        config: MongoDBConfig,
        db_name: str,
        collection_name: str,     
    ) -> motor.motor_asyncio.AsyncIOMotorCollection:
    """Create a new MongoDB collection."""
    client = motor.motor_asyncio.AsyncIOMotorClient(config.uri)
    db = client[db_name]
    collection = db[collection_name]
    return collection