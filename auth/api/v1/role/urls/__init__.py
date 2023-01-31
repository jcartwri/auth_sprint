from flask import Blueprint
from flask_restful import Api

api_role = Blueprint('role', __name__)
api_bp_role = Api(api_role)

from . import role
