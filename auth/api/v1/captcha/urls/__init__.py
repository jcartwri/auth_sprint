from flask import Blueprint
from flask_restful import Api

api_captcha = Blueprint('captcha', __name__)
api_bp_captcha = Api(api_captcha)

from . import captcha
