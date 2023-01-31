import http
from functools import wraps

from core import config
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from models.role import Role
from models.user import User
from models.user_role import UserRole


def is_admin_permissions():
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            if config.IS_TESTING:
                return func(*args, **kwargs)
            verify_jwt_in_request()
            user_id: str = get_jwt_identity()
            user = User.find_by_username(login=user_id['username'])
            user_roles = UserRole.query.filter_by(user_id=user.id).all()
            roles: list[str] = [Role.query.filter_by(id=i.role_id).first().role_name for i in user_roles]
            if config.ADMIN_USER in roles:
                return func(*args, **kwargs)
            else:
                return {
                    "message": "permission error",
                    "description": "Only for users, who has 'admin' role!",
                    "errors": [],
                }, http.HTTPStatus.FORBIDDEN

        return decorator

    return wrapper