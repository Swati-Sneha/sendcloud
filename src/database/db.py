from motor import motor_asyncio

from src.settings import settings
from src.utilities.singleton import SingletonMeta


class Database(metaclass=SingletonMeta):
    """Database Singleton Connector and configurator class."""

    def __init__(self) -> None:
        """Instance the db connection."""
        
        print("MONGO URL", settings.MONGO_URI)
        self.client = motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)
        self.db = self.client[settings.MONGO_DBNAME]
