from flask import Blueprint
from flask_restful import Api

api_auth = Blueprint('auth', __name__)
api_bp_auth = Api(api_auth)

from api.v1.auth.urls import auth
