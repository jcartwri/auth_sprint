from http import HTTPStatus

from circuitbreaker import circuit
from core.permissions import is_admin_permissions
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from models.user import User
from utils.decorators import rate_limit, tracing


class AllUsers(Resource):
    @jwt_required
    @circuit
    @is_admin_permissions()
    @rate_limit()
    @tracing
    def get(self):
        """
        Get all users
        ---
        tags:
          - User
        responses:
          200:
            description: Users were got
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
        return User.return_all(), HTTPStatus.OK

    @is_admin_permissions()
    @circuit
    def delete(self):
        """
        Delete all users
        ---
        tags:
          - User
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
        return User.delete_all(), HTTPStatus.OK
