import secrets
import string

from api.v1.oauth.viewsets.google import GoogleOAuth
from api.v1.oauth.viewsets.mail import MailOAuth
from api.v1.oauth.viewsets.yandex import YandexOAuth
from circuitbreaker import circuit
from flask import jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                set_refresh_cookies)
from models.auth_history import AuthHistory
from models.social_account import SocialAccount
from models.user import User
from transliterate import translit
from utils.decorators import error_exceptions
from utils.user_agent_parse import parsing

all_providers = {'yandex': YandexOAuth,
                 'mail': MailOAuth,
                 'google': GoogleOAuth}

CLIENT_IDS = {'yandex': 'client_id',
              'mail': 'client_id',
              'google': 'sub'}


def get_tokens(identifier: str, username: str):
    access_token = create_access_token(identity={'username': username,
                                                 'identifier': identifier})
    refresh_token = create_refresh_token(identity={'username': username,
                                                   'identifier': identifier})
    response = jsonify({'access_token': access_token, 'refresh_token': refresh_token})
    set_refresh_cookies(response, refresh_token)
    return response


def create_user(login: str, email: str, last_name: str, first_name: str) -> User:
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for _ in range(14))
    new_user = User(login=login, password=User.generate_hash(password),
                    email=email, last_name=last_name, first_name=first_name)
    new_user.save_to_db()
    return new_user


def create_social_account(social_id: str, provider_name: str, login: str,
                          email: str, last_name: str, first_name: str) -> tuple[User, SocialAccount]:
    new_user = create_user(login, email, last_name, first_name)
    new_social_acc = SocialAccount(user_id=new_user.id, social_id=social_id, social_name=provider_name)
    new_social_acc.save_to_db()
    return new_user, new_social_acc


def generate_login(last_name: str, first_name: str) -> str:
    alphabet = string.ascii_letters + string.digits
    login_part = ''.join(secrets.choice(alphabet) for _ in range(4))
    login = translit(last_name + first_name, 'ru', reversed=True).lower() + login_part
    return login


@error_exceptions
@circuit
def extract_data_from_providers(provider_name: str, data: dict):
    ua_string = request.headers.get('User-Agent')
    ua_device = parsing(ua_string)
    has_social_account = SocialAccount.find_row(data[CLIENT_IDS[provider_name]], provider_name)
    if not has_social_account:
        new_user = None
        if provider_name == 'yandex':
            new_user, _ = create_social_account(data['client_id'], provider_name, data['login'],
                                                data['emails'][0], data['last_name'], data['first_name'])

        elif provider_name == 'mail':
            login = generate_login(data['last_name'], data['first_name'])
            new_user, _ = create_social_account(data['client_id'], provider_name, login,
                                                data['email'], data['last_name'], data['first_name'])
        elif provider_name == 'google':
            login = generate_login(data['family_name'], data['given_name'])
            new_user, _ = create_social_account(data['sub'], provider_name, login, data['email'],
                                                data['family_name'], data['given_name'])

        auth_history = AuthHistory(user_id=new_user.id, user_agent=ua_string, user_device_type=ua_device)
        auth_history.save_to_db()
        return get_tokens(new_user.id, new_user.login)
    else:
        user = User.find_by_user_id(has_social_account.user_id)
        auth_history = AuthHistory(user_id=user.id, user_agent=ua_string, user_device_type=ua_device)
        auth_history.save_to_db()
        return get_tokens(user.id, user.login)

