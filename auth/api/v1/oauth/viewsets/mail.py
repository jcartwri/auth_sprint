from urllib.parse import urlencode

import requests
from api.v1.oauth.viewsets.base import BaseOAuth
from app import oauth
from core.config import TestSettings
from flask import request
from utils.decorators import error_exceptions

settings = TestSettings()


class MailOAuth(BaseOAuth):
    def __init__(self):
        super().__init__('mail')
        self.service = oauth.register(
            name=self.provider_name,
            client_id=self.client_id,
            client_secret=self.client_secret,
            authorize_url=settings.MAIL_AUTH_URL,
            response_type='code',
            scope="userinfo"
        )

    @error_exceptions
    def authorize(self) -> dict:
        token = requests.post(settings.MAIL_BASE_URL + "token",
                              params={
                                  'client_id': settings.MAIL_CLIENT_ID,
                                  'client_secret': settings.MAIL_CLIENT_SECRET
                              },
                              data=urlencode({
                                  'grant_type': 'authorization_code',
                                  'code': request.args.get('code'),
                                  'redirect_uri': settings.MAIL_REDIRECT_URI})).json()
        return token

    @error_exceptions
    def get_user_info(self, token: dict) -> dict:
        return requests.get(settings.MAIL_INFO_URL,
                            {'access_token': token['access_token']}).json()
