from http import HTTPStatus

from circuitbreaker import circuit
from core.permissions import is_admin_permissions
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from models.role import Role
from utils.decorators import tracing


class ShowRoles(Resource):
    @tracing
    @circuit
    @jwt_required()
    @is_admin_permissions()
    def get(self):
        """
        Get all roles
        ---
        tags:
          - Role
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
        result = [
            {
                "id": str(role.id),
                "role_name": role.role_name,
                "date": str(role.register_date)
            }
            for role in Role.query.filter().all()
        ]
        return result, HTTPStatus.OK
