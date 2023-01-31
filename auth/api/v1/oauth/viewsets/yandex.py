from urllib.parse import urlencode

import requests
from api.v1.oauth.viewsets.base import BaseOAuth
from app import oauth
from core.config import TestSettings
from flask import request
from utils.decorators import error_exceptions

settings = TestSettings()


class YandexOAuth(BaseOAuth):
    def __init__(self):
        super().__init__('yandex')
        self.service = oauth.register(
            name=self.provider_name,
            client_id=self.client_id,
            client_secret=self.client_secret,
            authorize_url=settings.YANDEX_AUTH_URL,
            response_type='code',
            display="popup",
            scope="login:email login:info"
        )

    @error_exceptions
    def authorize(self) -> dict:
        parameters = urlencode({
            'grant_type': 'authorization_code',
            'code': request.args.get('code'),
            'client_id': settings.YANDEX_CLIENT_ID,
            'client_secret': settings.YANDEX_CLIENT_SECRET
        })
        token = requests.post(settings.YANDEX_BASE_URL + "token", parameters).json()
        return token

    @error_exceptions
    def get_user_info(self, token: dict) -> dict:
        return requests.get(settings.YANDEX_INFO_URL, {
            'with_openid_identity': 'true',
            'oauth_token': token['access_token']}).json()
