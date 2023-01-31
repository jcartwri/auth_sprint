from http import HTTPStatus

from api.v1.messages import USER_ROLE_NOT_EX
from circuitbreaker import circuit
from core.permissions import is_admin_permissions
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.role import Role
from models.user import User
from models.user_role import UserRole
from utils.decorators import tracing

parser = reqparse.RequestParser()
parser.add_argument(
    "role_name", type=str, help="This field cannot be blank", required=True, trim=True
)
parser.add_argument(
    "user_login", type=str, help="This field cannot be blank", default=None, trim=True
)


class ShowUserRole(Resource):
    @circuit
    @tracing
    @jwt_required()
    @is_admin_permissions()
    def get(self):
        """
        Get some user_role
        ---
        tags:
          - User_Role
        parameters:
          - in: body
            name: body
            schema:
              id: RoleName
              required:
                - role_name
                - user_login
              properties:
                role_name:
                  type: string
                  description: Name of role.
                user_login:
                  type: string
                  description: Username.
              example:
                role_name: test_role
                user_login: DoctorWho
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
        data: reqparse.Namespace = parser.parse_args()
        user_login: str = data.get("user_login", None)
        role_name: str = data.get("role_name", None)

        if user_login and role_name:
            role = Role.find_by_role_name(role_name=role_name)
            user = User.find_by_username(login=user_login)
            user_role = UserRole(user_id=user.id, role_id=role.id)
            result = {
                "id": str(user_role.id),
                "role_id": str(user_role.role_id),
                "user_id": str(user_role.user_id)
            }
            return result, HTTPStatus.OK
        else:
            return {
                       "message": "wrong data",
                       "errors": [{"name": USER_ROLE_NOT_EX.format(role_name, user_login)}],
            }, HTTPStatus.BAD_REQUEST
