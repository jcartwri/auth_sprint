from api.v1.oauth.viewsets.base import BaseOAuth
from app import oauth
from core.config import TestSettings
from utils.decorators import error_exceptions

settings = TestSettings()


class GoogleOAuth(BaseOAuth):
    def __init__(self):
        super().__init__('google')
        self.service = oauth.register(
            name=self.provider_name,
            client_id=self.client_id,
            client_secret=self.client_secret,
            server_metadata_url=settings.GOOGLE_CONF_URL,
            client_kwargs={
                'scope': 'openid email profile'
            }
        )

    @error_exceptions
    def authorize(self) -> dict:
        token = self.service.authorize_access_token()
        return token

    @error_exceptions
    def get_user_info(self, token: dict) -> dict:
        return token['userinfo']
