from flask import jsonify
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required)
from flask_restful import Resource
from utils.decorators import rate_limit, tracing


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    @tracing
    @rate_limit()
    def post(self):
        """
        Refresh token
        ---
        tags:
          - Authorization
        responses:
          200:
            description: Access token was received
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
            description: Unauthorised response
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
        access_token = create_access_token(identity=current_user)
        response = jsonify({'access_token': access_token})
        # set_access_cookies(response, access_token)
        return response
