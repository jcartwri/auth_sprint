from api.v1.oauth.settings import extract_data_from_providers
from flask import Blueprint
from utils.decorators import tracing

oauth = Blueprint("oauth", __name__)


@tracing
@oauth.route('/login/<provider>/')
def service_auth(provider: str):
    from api.v1.oauth.settings import all_providers

    oauth_client = all_providers[provider]()
    return oauth_client.redirect_url()


@tracing
@oauth.route('/login/<provider>/auth')
def oauth_callback(provider: str):
    from api.v1.oauth.settings import all_providers

    oauth_client = all_providers[provider]()
    token = oauth_client.authorize()
    data = oauth_client.get_user_info(token)
    result = extract_data_from_providers(provider, data)
    return result
