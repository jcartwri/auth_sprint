from http import HTTPStatus

from api.v1.messages import USER_NOT_EX
from circuitbreaker import circuit
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.captcha import Captcha
from models.user import User
from utils.decorators import tracing

parser = reqparse.RequestParser()

parser.add_argument(
    "answear", type=str, help="This field cannot be blank", required=True, trim=True
)

parser.add_argument(
    "user_login", type=str, help="This field cannot be blank", required=True, trim=True
)


class CheckCaptcha(Resource):
    @circuit
    @tracing
    @jwt_required()
    def post(self):
        """
        Cheack Captcha
        ---
        tags:
          - Captcha
        parameters:
          - in: body
            name: body
            schema:
              id: Captcha
              required:
                - answear
                - user_login
              properties:
                answear:
                  type: string
                  description: Answear from User.
                  default: "ansear"
                user_login:
                  type: string
                  description: User login.
                  default: "admin"
              example:
                answear: ansear
                user_login: admin
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

        user = User.find_by_username(login=data.get("user_login"))
        if not user:
            return {
                       "message": "wrong data",
                       "errors": [{"name": USER_NOT_EX.format(data.get("user_login"))}],
                   }, HTTPStatus.BAD_REQUEST

        is_cap_old = user.id in [cap.user_id for cap in Captcha.query.all()]
        if not is_cap_old:
            return {
                "message": "wrong data",
                "errors": [{"name": USER_NOT_EX.format(data.get("user_login"))}],
            }, HTTPStatus.BAD_REQUEST
        cap = Captcha.query.filter_by(user_id=user.id).first()
        if cap.captcha == data.get("answear"):
            return {"value": True}, HTTPStatus.OK
        else:
            return {"value": False}, HTTPStatus.FORBIDDEN



