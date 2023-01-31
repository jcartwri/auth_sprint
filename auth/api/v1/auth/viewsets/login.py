from http import HTTPStatus

from api.v1.messages import USER_NOT_EX, WRONG_CREDENTIALS
from circuitbreaker import circuit
from flask import jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                set_refresh_cookies)
from flask_restful import Resource, reqparse
from models.auth_history import AuthHistory
from models.user import User
from utils.decorators import tracing
from utils.user_agent_parse import parsing

parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)


class UserLogin(Resource):
    @tracing
    @circuit
    def post(self):
        """
        User's login
        ---
        tags:
          - Authorization
        parameters:
          - in: body
            name: body
            schema:
              id: UserLogin
              required:
                - username
                - password
              properties:
                username:
                  type: string
                  description: Username.
                  default: "DoctorWho"
                password:
                  type: string
                  description: Password.
                  default: "asdAQW123"
              example:
                username: DoctorWho
                password: asdAQW123
        responses:
          200:
            description: User was logged in
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
          404:
            description: User not found response
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
                  description: Errors
                  items:
                    type: object
                    default: ...
                  default: []
                message:
                  type: string
                  description: Response message
        """
        data: reqparse.Namespace = parser.parse_args()
        user_search = User.find_by_username(data['username'])

        if not user_search:
            return {'message': USER_NOT_EX.format(data['username'])}, HTTPStatus.NOT_FOUND
        if User.verify_hash(data['password'], user_search.password):
            ua_string = request.headers.get('User-Agent')
            ua_device = parsing(ua_string)

            auth_history = AuthHistory(user_id=user_search.id,
                                       user_agent=ua_string,
                                       user_device_type=ua_device)
            auth_history.save_to_db()
            access_token = create_access_token(identity={'username': data['username'],
                                                         'identifier': user_search.id})
            refresh_token = create_refresh_token(identity={'username': data['username'],
                                                           'identifier': user_search.id})
            response = jsonify({'access_token': access_token, 'refresh_token': refresh_token})

            set_refresh_cookies(response, refresh_token)
            return response
        else:
            return {'message': WRONG_CREDENTIALS}, HTTPStatus.FORBIDDEN
