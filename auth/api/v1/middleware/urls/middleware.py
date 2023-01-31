from ..viewsets import get_username, get_user_id
from . import api_bp_middleware

api_bp_middleware.add_resource(get_username.GetUsername, "/get_username")
api_bp_middleware.add_resource(get_user_id.GetUserId, "/get_user_id")
