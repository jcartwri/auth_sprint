from datetime import timedelta

from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    REDIS_HOST: str = Field("127.0.0.1", env="REDIS_HOST")
    REDIS_PORT: str = Field("6379", env="REDIS_PORT")
    JWT_SECRET_KEY: str = Field("secret-key", env="JWT_SECRET_KEY")
    APP_SECRET_KEY: str = Field("secret-key-app-qqq", env="APP_SECRET_KEY")
    DB_URI: str = Field("postgresql://app:123qwe@0.0.0.0/movies_db", env="DB_URI")

    SERVICE_HOST: str = Field('127.0.0.1', env='SERVICE_HOST')
    SERVICE_PORT: str = Field('5000', env='SERVICE_PORT')

    MAIL_CLIENT_SECRET: str = Field('79ea7e344a8d4e14a47e36e1e411181c', env='MAIL_CLIENT_SECRET')
    MAIL_CLIENT_ID: str = Field('82444185d7a8452282b2888cd9e8bd28', env='MAIL_CLIENT_ID')
    MAIL_INFO_URL: str = Field('https://o2.mail.ru/userinfo', env='MAIL_INFO_URL')
    MAIL_REDIRECT_URI: str = Field('http://127.0.0.1:5000/login/mail/auth', env='MAIL_REDIRECT_URI')
    MAIL_BASE_URL: str = Field('https://o2.mail.ru/', env='MAIL_BASE_URL')
    MAIL_AUTH_URL: str = Field('https://oauth.mail.ru/login', env='MAIL_AUTH_URL')

    YANDEX_CLIENT_SECRET: str = Field('8b9bfed8523142efa6210dac4856f6f3', env='YANDEX_CLIENT_SECRET')
    YANDEX_CLIENT_ID: str = Field('c73509d87c7e4e7d8e5a99cb6be73f2a', env='YANDEX_CLIENT_ID')
    YANDEX_AUTH_URL: str = Field('https://oauth.yandex.ru/authorize', env='YANDEX_AUTH_URL')
    YANDEX_BASE_URL: str = Field('https://oauth.yandex.ru/', env='YANDEX_BASE_URL')
    YANDEX_INFO_URL: str = Field('https://login.yandex.ru/info', env='YANDEX_INFO_URL')

    GOOGLE_CLIENT_SECRET: str = Field('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', env='GOOGLE_CLIENT_SECRET')
    GOOGLE_CLIENT_ID: str = Field('346840914362-o9nvfd03p7ihtclocq0ad89k93odtdhc.apps.googleusercontent.com',
                                  env='GOOGLE_CLIENT_ID')
    GOOGLE_CONF_URL: str = Field('https://accounts.google.com/.well-known/openid-configuration', env='GOOGLE_CONF_URL')

    JAEGER_HOST: str = Field('localhost', env='JAEGER_HOST')
    JAEGER_PORT: str = Field('6831', env='JAEGER_PORT')
    enabled_tracing: bool = Field('True', env='ENABLED_TRACING')


IS_TESTING: bool = True


SPECIAL_ROLE = "subscriber"

ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
ADMIN_USER: str = "admin"
