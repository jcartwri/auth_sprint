import abc

from core.config import TestSettings
from flask import url_for

settings = TestSettings()


OAUTH_CREDENTIALS = {
    'google': {
        'id': settings.GOOGLE_CLIENT_ID,
        'secret': settings.GOOGLE_CLIENT_SECRET
    },
    'mail': {
        'id': settings.MAIL_CLIENT_ID,
        'secret': settings.MAIL_CLIENT_SECRET
    },
    'yandex': {

        'id': settings.YANDEX_CLIENT_ID,
        'secret': settings.YANDEX_CLIENT_SECRET
    }
}


class BaseOAuth:
    def __init__(self, provider_name: str):
        self.provider_name = provider_name
        credentials = OAUTH_CREDENTIALS[provider_name]
        self.client_id = credentials['id']
        self.client_secret = credentials['secret']
        self.service = None

    @abc.abstractmethod
    def authorize(self) -> dict:
        pass

    @abc.abstractmethod
    def get_user_info(self, token: dict) -> dict:
        pass

    def redirect_url(self):
        redirect_uri: str = url_for(
            "oauth.oauth_callback", _external=True, provider=self.provider_name
        )
        return self.service.authorize_redirect(redirect_uri=redirect_uri)
