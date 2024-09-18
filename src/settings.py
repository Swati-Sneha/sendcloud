import enum
import pydantic_settings
from pydantic import Field

class SendCloudEnvironment(str, enum.Enum):
    LOCAL = "local"
    TESTING = "testing"


class Settings(pydantic_settings.BaseSettings):
    SENDCLOUD_ENVIRONMENT: SendCloudEnvironment = Field(default=SendCloudEnvironment.LOCAL, description="Deployment environment")

    RABBITMQ_USER: str = Field(default="localUser", description="RabbitMQ User")
    RABBITMQ_PASSWORD: str = Field(default="localPass", description="RabbitMQ Password")
    DEFAULT_BROKER: str = Field(default=f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@rabbitmq:5672")

    CELERY_BROKER_URL: str = Field(default=f"amqp://localhost", description="Celery Broker URL")
    CELERY_APP_NAME: str = Field(default="timer", description="Celery App Name")
    CELERY_RESULT_BACKEND: str = Field(default="", description="Celery Result Backend")

    CELERY_TASK_ALWAYS_EAGER: bool = Field(default=True)
    CELERY_TASK_EAGER_PROPAGATES: bool = Field(default=True)
    
    MONGO_PROTOCOL: str = Field(default="mongodb", description="Mongo DB Protocol")
    MONGO_HOST: str = Field(default="mongodb", description="Mongo Db Host")
    MONGO_PORT: int =  Field(default=27017, description="Mongo Db Port")
    MONGO_HOSTS: str = Field(default=f"{MONGO_HOST} : {str(MONGO_PORT)}", description="Mongo Db Hosts")
    MONGO_USERNAME: str = Field(default="localUser", description="Mongo Db UserName")
    MONGO_PASSWORD: str = Field(default="localPass", description="MongoDb Password")
    MONGO_DBNAME: str = Field(default="timer", description= "Mongodb name")
    
    MONGO_URI: str = Field(default=f"{MONGO_PROTOCOL}://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOSTS}/{MONGO_DBNAME}", description="Mongo URI")
    

    class Config:
        env_file = ".env" 
        
        
settings = Settings()