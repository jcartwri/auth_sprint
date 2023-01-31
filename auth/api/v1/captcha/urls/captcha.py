from ..viewsets import check_captcha, create_captcha
from . import api_bp_captcha

api_bp_captcha.add_resource(create_captcha.CreateCaptcha, "/captcha/create")
api_bp_captcha.add_resource(check_captcha.CheckCaptcha, "/captcha/check")