from http import HTTPStatus

from api.v1.messages import ROLE_CREATE, ROLE_EX, ROLE_EXEPTION
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


class CreateRole(Resource):
    @circuit
    @tracing
    @jwt_required()
    @is_admin_permissions()
    def post(self):
        """
        Create new role
        ---
        tags:
          - Role
        parameters:
          - in: body
            name: body
            schema:
              id: RoleName
              required:
                - role_name
              properties:
                role_name:
                  type: string
                  description: Name of role.
                  default: "reader"
        responses:
          200:
            description: Role was created
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
          400:
            description: Bad request response
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
          409:
            description: Conflict response
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
                  description: Role already exists
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
        if not role_name:
            return {
                       "message": "wrong data",
                       "errors": [{"name": ROLE_EXEPTION}],
            }, HTTPStatus.BAD_REQUEST
        if not Role.by_name_exist(role_name=role_name):
            new_role = Role(role_name=role_name)
            new_role.save_to_db()
            return {'message': ROLE_CREATE.format(role_name)}, HTTPStatus.OK
        return {
            "message": "wrong data",
            "errors": [{"name": ROLE_EX.format(role_name)}],
        }, HTTPStatus.BAD_REQUEST