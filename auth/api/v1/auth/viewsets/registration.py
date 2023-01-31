from http import HTTPStatus

from api.v1.messages import (INTERNAL_SERVER_ERROR, INVALID_PASSWORD,
                             USER_CREATE, USER_EX)
from circuitbreaker import circuit
from email_validator import EmailNotValidError, validate_email
from flask_restful import Resource, reqparse
from models.user import User
from utils.decorators import tracing
from utils.validator import schema

parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)
parser.add_argument('email', help='This field cannot be blank', required=True)
parser.add_argument('last_name', help='This field cannot be blank', required=True)
parser.add_argument('first_name', help='This field cannot be blank', required=True)


class UserRegistration(Resource):
    @circuit
    @tracing
    def post(self):
        """
        User's registration
        ---
        tags:
          - Authorization
        parameters:
          - in: body
            name: body
            schema:
              id: UserRegistration
              required:
                - username
                - password
                - email
                - last_name
                - first_name
              properties:
                username:
                  type: string
                  description: Username.
                  default: "DoctorWho"
                password:
                  type: string
                  description: Password.
                  default: "asdAQW123"
                email:
                  type: string
                  description: Email
                  default: "asdfer@mail.com"
                last_name:
                  type: string
                  description: Last name
                  default: "John"
                first_name:
                  type: string
                  description: First name
                  default: "Do"
              example:
                username: DoctorWho
                password: asdAQW123
                email: asdfer@mail.com
                last_name: John
                first_name: Do
        responses:
          200:
            description: User was created
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
        new_user = User(
            login=data['username'],
            password=User.generate_hash(data['password']),
            email=data['email'],
            last_name=data['last_name'],
            first_name=data['first_name']
        )

        if User.find_by_username(data['username']):
            return {'message': USER_EX.format(data['username'])}, HTTPStatus.CONFLICT

        try:
            validate_email(data['email'])
        except EmailNotValidError as e:
            return {'message': str(e)}, HTTPStatus.BAD_REQUEST

        if not schema.validate(data['password']):
            return {'message': INVALID_PASSWORD}, HTTPStatus.BAD_REQUEST

        try:
            new_user.save_to_db()

            return {'message': USER_CREATE.format(data['username'])}, HTTPStatus.OK
        except Exception:
            return {'message': INTERNAL_SERVER_ERROR}, HTTPStatus.INTERNAL_SERVER_ERROR
