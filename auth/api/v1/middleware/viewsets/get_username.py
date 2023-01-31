from http import HTTPStatus

from core.config import SPECIAL_ROLE
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required)
from flask_restful import Resource
from models.role import Role
from models.user import User
from models.user_role import UserRole


class GetUsername(Resource):
    @jwt_required()
    def get(self):
        """
        Get username
        ---
        tags:
          - GetUsername
        parameters:
          - in: body
            name: body
            schema:
              id: GetUsername
              required:
                - header
              properties:
                header:
                  type: string
                  description: Name of role.
              example:
                header: fafafadfwretwegtfscg
        responses:
          200:
            description: Roles were got
            schema:
              properties:
                success:
                  type: boolean
                  description: Response status
                  default: True
                data:
                  type: array
                  description: Response data
                  items:
                    type: object
                    default: ...
                  default: []
                message:
                  type: string
                  description: Response message
          401:
            description: Unauthorized response
            schema:
              properties:
                success:
                  type: boolean
                  description: Response status
                  default: False
                data:
                  type: array
                  description: Response data
                  items:
                    type: object
                    default: ...
                  default: []
                errors:
                  type: array
                  description: Data with error validation messages
                  items:
                    type: object
                    default: ...
                  default: []
                message:
                  type: string
                  description: Response message
        """
        current_user = get_jwt_identity()
        user_name = current_user.get("username")
        print('user_name', user_name, current_user)
        user = User.find_by_username(login=user_name)
        print('user', user)
        user_roles = [
            Role.query.filter_by(id=user_role.role_id).first().role_name
            for user_role in UserRole.query.filter_by(user_id=user.id).all()
        ]

        is_user = user is None
        print('is_user', is_user)
        print('user_roles', user_roles)
        is_special_role = SPECIAL_ROLE not in user_roles
        print('is_special_role', is_special_role)

        if is_user or is_special_role:
            user_name = None

        return {"username": user_name}, HTTPStatus.OK

