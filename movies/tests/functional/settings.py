from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    redis_host: str = Field("127.0.0.1", env="REDIS_HOST")
    redis_port: str = Field("6379", env="REDIS_PORT")
    es_host: str = Field("127.0.0.1", env="ELASTIC_HOST")
    es_port: str = Field("9200", env="ELASTIC_PORT")
    service_host: str = Field('127.0.0.1', env='SERVICE_HOST')
    service_port: str = Field('8000', env='SERVICE_PORT')
    AUTH_SERVICE_HOST: str = Field('127.0.0.1', env='SERVICE_HOST')
    AUTH_SERVICE_PORT: str = Field('5000', env='SERVICE_PORT')
    AUTH_SERVICE_URL: str = Field('http://0.0.0.0:5000/', env='SERVICE_URL')
