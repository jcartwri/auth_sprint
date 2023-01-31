import uuid
from http import HTTPStatus

from captcha.image import ImageCaptcha
from circuitbreaker import circuit
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.captcha import Captcha
from models.user import User
from utils.decorators import tracing

parser = reqparse.RequestParser()

parser.add_argument(
    "user_login", type=str, help="This field cannot be blank", required=True, trim=True
)

parser.add_argument(
    "word", type=str, help="This field cannot be blank", trim=True
)


class CreateCaptcha(Resource):
    @circuit
    @tracing
    @jwt_required()
    def post(self):
        """
        Create Captcha
        ---
        tags:
          - Captcha
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
        image = ImageCaptcha(width=280, height=90)

        from random_word import RandomWords
        r = RandomWords()
        word = data.get("word", None)
        word = word if word else r.get_random_word()
        res = image.generate(word)

        user = User.find_by_username(login=data.get("user_login"))

        is_cap_old = user.id in [cap.user_id for cap in Captcha.query.all()]
        if is_cap_old:
            Captcha.delete_by_id(uuid.UUID(str(user.id)))
        Captcha(captcha=word, user_id=uuid.UUID(str(user.id))).save_to_db()
        return str(int.from_bytes(res.getvalue(), byteorder='little')), HTTPStatus.OK
