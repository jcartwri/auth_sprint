from flask import Blueprint
from flask_restful import Api

api_middleware = Blueprint('middleware', __name__)
api_bp_middleware = Api(api_middleware)

from . import middleware
