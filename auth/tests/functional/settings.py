from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    REDIS_HOST: str = Field("127.0.0.1", env="REDIS_HOST")
    REDIS_PORT: str = Field("6379", env="REDIS_PORT")
    JWT_SECRET_KEY: str = Field("secret-key", env="JWT_SECRET_KEY")
    APP_SECRET_KEY: str = Field("secret-key-app", env="APP_SECRET_KEY")
    DB_URI: str = Field("postgresql://app:123qwe@0.0.0.0/movies_db", env="DB_URI")

    SERVICE_HOST: str = Field('127.0.0.1', env='SERVICE_HOST')
    SERVICE_PORT: str = Field('5000', env='SERVICE_PORT')
    SERVICE_URL: str = Field('http://0.0.0.0:5000/', env='SERVICE_URL')

