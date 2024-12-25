from os import environ as env

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv(".env-non-dev")


class RabbitMQConfig(BaseModel):
    host: str = Field(alias="RABBITMQ_HOST")
    port: int = Field(alias="RABBITMQ_PORT")
    login: str = Field(alias="RABBITMQ_USER")
    password: str = Field(alias="RABBITMQ_PASS")


class PostgresConfig(BaseModel):
    host: str = Field(alias="TEST_POSTGRES_HOST")
    port: int = Field(alias="TEST_POSTGRES_PORT")
    login: str = Field(alias="TEST_POSTGRES_USER")
    password: str = Field(alias="TEST_POSTGRES_PASSWORD")
    database: str = Field(alias="TEST_POSTGRES_DB")

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.login}:{self.password}@{self.host}:{self.port}/{self.database}"


class JWTConfig(BaseModel):
    SECRET_KEY: str = Field(alias="SECRET_KEY")
    ALGORITHM: str = Field(alias="ALGORITHM")
    ACCESS_TOKEN_EXPIRES_MINUTES: int = Field(alias="ACCESS_TOKEN_EXPIRES_MINUTES")
    REFRESH_TOKEN_EXPIRES_MINUTES: int = Field(alias="REFRESH_TOKEN_EXPIRES_MINUTES")


class Config(BaseModel):
    rabbitmq: RabbitMQConfig = Field(default_factory=lambda: RabbitMQConfig(**env))
    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig(**env))
    JWT_Config: JWTConfig = Field(default_factory=lambda: JWTConfig(**env))


def get_postgres_config():
    return PostgresConfig(**env)
