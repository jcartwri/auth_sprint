from http import HTTPStatus

from api.v1.messages import ROLE_CHANGE, ROLE_NOT_EX
from circuitbreaker import circuit
from core.permissions import is_admin_permissions
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.role import Role
from utils.decorators import tracing

parser = reqparse.RequestParser()
parser.add_argument(
    "old_role_name", type=str, help="This field cannot be blank", required=True, trim=True
)

parser.add_argument(
    "new_role_name", type=str, help="This field cannot be blank", required=True, trim=True
)


class ChangeRole(Resource):
    @circuit
    @tracing
    @jwt_required()
    @is_admin_permissions()
    def post(self):
        """
        Change role
        ---
        tags:
          - Role
        parameters:
          - in: body
            name: body
            schema:
              id: RoleChange
              required:
                - old_role_name
                - new_role_name
              properties:
                old_role_name:
                  type: string
                  description: Old name for role.
                  default: "test_role"
                new_role_name:
                  type: string
                  description: New name for role.
                  default: "prod_role"
              example:
                old_role_name: test_role
                new_role_name: prod_role
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
                  description: User already exists
                  items:
                    type: object
                    default: ...
                  default: []
                message:
                  type: string
                  description: Response message

        """
        data: reqparse.Namespace = parser.parse_args()
        old_role_name: str = data.get("old_role_name")
        new_role_name: str = data.get("new_role_name")

        if Role.by_name_exist(role_name=old_role_name):
            role = Role.query.filter_by(role_name=old_role_name).first()
            role.role_name = new_role_name
            role.save_to_db()
            return {'message': ROLE_CHANGE.format(old_role_name, new_role_name)}, HTTPStatus.OK
        return {
                   "message": "wrong data",
                   "errors": [{"name": ROLE_NOT_EX.format(old_role_name)}],
               }, HTTPStatus.BAD_REQUEST
