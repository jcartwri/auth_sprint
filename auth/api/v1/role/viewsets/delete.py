from http import HTTPStatus

from api.v1.messages import ROLE_DELETE, ROLE_NOT_DELETE
from circuitbreaker import circuit
from core.permissions import is_admin_permissions
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.role import Role
from utils.decorators import tracing

parser = reqparse.RequestParser()
parser.add_argument(
    "role_name", type=str, help="This field cannot be blank", required=True, trim=True
)


class DeleteRole(Resource):
    @tracing
    @circuit
    @jwt_required()
    @is_admin_permissions()
    def delete(self):
        """
        Delete role
        ---
        tags:
          - Role
        parameters:
          - in: body
            name: body
            schema:
              id: RoleDelete
              required:
                - role_name
              properties:
                role_name:
                  type: string
                  description: Old name for role.
                  default: "test_role"
              example:
                role_name: test_role

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
        role_name: str = data.get("role_name")
        if Role.by_name_exist(role_name=role_name):
            role = Role.query.filter_by(role_name=role_name).first()
            Role.delete_by_id(role.id)
            return {'message': ROLE_DELETE.format(role_name)}, HTTPStatus.OK
        return {
                   "message": "wrong data",
                   "errors": [{"name": ROLE_NOT_DELETE.format(role_name)}],
               }, HTTPStatus.BAD_REQUEST


class DeleteAllRoles(Resource):
    @is_admin_permissions()
    @circuit
    def delete(self):
        """
        Delete all roles
        ---
        tags:
          - Role
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
        return Role.delete_all(), HTTPStatus.OK
