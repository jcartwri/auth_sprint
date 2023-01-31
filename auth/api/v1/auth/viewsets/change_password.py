from http import HTTPStatus

from api.v1.messages import CHANGED_PASSWORD, WRONG_PASSWORD
from circuitbreaker import circuit
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse
from models.user import User
from utils.decorators import tracing

parser = reqparse.RequestParser()
parser.add_argument('old_password', help='This field cannot be blank', required=True)
parser.add_argument('new_password', help='This field cannot be blank', required=True)


class ChangePassword(Resource):
    @jwt_required()
    @tracing
    @circuit
    def post(self):
        """
        Change user's password
        ---
        tags:
          - Authorization
        parameters:
          - in: body
            name: body
            schema:
              id: ChangePassword
              required:
                - old_password
                - new_password
              properties:

                old_password:
                  type: string
                  description: Old password.
                  default: "asdAQW123"
                new_password:
                  type: string
                  description: New password.
                  default: "edAQW1234"
              example:
                old_password: asdAQW123
                new_password: edAQW1234
        responses:
          200:
            description: Password were changed
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
          403:
            description: Forbidden response
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
        user_id: str = get_jwt_identity()['identifier']
        user = User.find_by_user_id(user_id)
        if User.verify_hash(data['old_password'], user.password):
            user.change_credential(password=data['new_password'])
            user.save_to_db()
            return {'message': CHANGED_PASSWORD}, HTTPStatus.OK
        else:
            return {'message': WRONG_PASSWORD}, HTTPStatus.FORBIDDEN


class ResetPassword:
    pass

