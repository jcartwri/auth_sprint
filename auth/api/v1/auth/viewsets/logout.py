from api.v1.messages import TOKEN_REVOKED
from circuitbreaker import circuit
from core.config import ACCESS_TOKEN_EXPIRES
from database.redis_cache import redis_cache
from flask import jsonify
from flask_jwt_extended import get_jwt, jwt_required, unset_jwt_cookies
from flask_restful import Resource
from utils.decorators import tracing


class UserLogoutAccess(Resource):
    @circuit
    @jwt_required()
    @tracing
    def post(self):
        """
        User logout
        ---
        tags:
          - Authorization
        responses:
          200:
            description: User has been logged out
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
        jti: str = get_jwt()["jti"]
        redis_cache.set(jti, "", ex=ACCESS_TOKEN_EXPIRES)
        res = jsonify({'message': TOKEN_REVOKED})
        unset_jwt_cookies(res)
        return res

