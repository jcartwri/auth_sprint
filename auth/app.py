import click
from authlib.integrations.flask_client import OAuth
from core.config import ADMIN_USER, IS_TESTING, TestSettings
from database.db import db
from flasgger import Swagger
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from models.auth_history import AuthHistory
from models.captcha import Captcha
from models.role import Role
from models.social_account import SocialAccount
from models.user import User
from models.user_role import UserRole
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from utils import exceptions

settings = TestSettings()

app = Flask(__name__)

if settings.enabled_tracing:
    FlaskInstrumentor().instrument_app(app)
    RequestsInstrumentor().instrument()

swagger = Swagger(app, template={
        "swagger": "2.0",
        "info": {
            "title": "Authentication API",
            "description": "Authentication API for movies service",
            "version": "1.0",
        },
        "consumes": [
            "application/json",
        ],
        "produces": [
            "application/json",
        ],
        "securityDefinitions": {"Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}},
        "security": [{"Bearer": []}],

    })


app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
# app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY
app.secret_key = settings.APP_SECRET_KEY

api = Api(app)

migrate = Migrate(app, db)
db.init_app(app)

oauth = OAuth(app)
oauth.init_app(app)


@app.cli.command("create_admin")
@click.argument("username")
@click.argument("password")
@click.argument("email")
@click.argument("last_name")
@click.argument("first_name")
def create_admin(username: str, password: str, email: str, last_name: str, first_name: str):
    """create new user with admin role"""
    if not IS_TESTING:
        new_user = User(login=username,
                        password=User.generate_hash(password),
                        email=email,
                        last_name=last_name,
                        first_name=first_name
                        )
        new_user.save_to_db()
        """ find admin role """
        try:
            role_admin = Role.find_by_role_name(role_name=ADMIN_USER)
        except Exception:
            role_admin = Role(role_admin=ADMIN_USER)
            role_admin.save_to_db()

        """ set admin role for user """
        new_user_role = UserRole(user_id=new_user.id, role_id=role_admin.id)
        new_user_role.save_to_db()


def launch_app(app_auth):
    from api.v1.auth.urls import api_auth
    from api.v1.captcha.urls import api_captcha
    from api.v1.middleware.urls import api_middleware
    from api.v1.oauth.urls.oauth import oauth
    from api.v1.role.urls import api_role
    from api.v1.user_role.urls import api_user_role
    from database.db import db, init_db, jwt
    app.register_blueprint(api_auth)
    app.register_blueprint(api_role)
    app.register_blueprint(api_user_role)
    app.register_blueprint(oauth)
    app.register_blueprint(api_captcha)
    app.register_blueprint(api_middleware)

    db.init_app(app=app_auth)
    # with app.app_context():
    #     db.create_all()
    jwt.init_app(app=app_auth)

    # @app.before_request
    # def before_request():
    #     request_id = request.headers.get('X-Request-Id')
    #     if not request_id:
    #         raise RuntimeError('request id is required')

    app_auth.run(host='0.0.0.0', debug=True)
    # app_auth.run(host='127.0.0.1', port=5000, debug=True)


if __name__ == '__main__':
    launch_app(app_auth=app)

