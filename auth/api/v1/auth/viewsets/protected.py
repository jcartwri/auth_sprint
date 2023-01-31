from http import HTTPStatus

from api.v1.messages import TOKEN_ACCEPTED
from circuitbreaker import circuit
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from utils.decorators import rate_limit, tracing


class SecretResource(Resource):
    @jwt_required()
    @circuit
    @tracing
    @rate_limit()
    def get(self):
        """
        Check user has access to system
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
        return {
            'answer': TOKEN_ACCEPTED
        }, HTTPStatus.OK
