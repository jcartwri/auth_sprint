import uuid
from http import HTTPStatus

from api.v1.messages import USER_ROLE_DELETE, USER_ROLE_NOT_EX
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
    "user_login", type=str, help="This field cannot be blank", required=True, trim=True
)


class DeleteUserRole(Resource):
    @circuit
    @tracing
    @jwt_required()
    @is_admin_permissions()
    def delete(self):
        """
        Delete
        ---
        tags:
          - User_Role
        responses:
          200:
            description: User has access
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

        role = Role.find_by_role_name(role_name=role_name)
        user = User.find_by_username(login=user_login)

        if role and user and UserRole.is_row_exist(user_id=uuid.UUID(str(user.id)),
                                                   role_id=uuid.UUID(str(role.id))):
            user_role = UserRole.get_row_by_ids(user_id=user.id, role_id=role.id)
            UserRole.delete_by_id(uuid.UUID(str(user_role.id)))
            return {'message': USER_ROLE_DELETE.format(user_login, role_name)}, HTTPStatus.OK
        return {
                   "message": "wrong data",
                   "errors": [{"name": USER_ROLE_NOT_EX.format(role_name, user_login)}],
        }, HTTPStatus.BAD_REQUEST


class DeleteAllUserRoles(Resource):
    @circuit
    @tracing
    @is_admin_permissions()
    def delete(self):
        """
        Delete all roles
        ---
        tags:
          - User_Role
        responses:
          200:
            description: Roles was deleted
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
        return UserRole.delete_all(), HTTPStatus.OK
