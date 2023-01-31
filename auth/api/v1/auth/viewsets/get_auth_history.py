from http import HTTPStatus

from api.v1.messages import AUTH_HISTORY_NEX, PAGE_NOT_FOUND
from core.permissions import is_admin_permissions
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse
from models.auth_history import AuthHistory
from utils.decorators import rate_limit, tracing
from werkzeug import exceptions

parser = reqparse.RequestParser()
parser.add_argument('page_number', help='This field cannot be blank', required=False)


class GetAuthHistory(Resource):
    @jwt_required()
    @tracing
    @rate_limit()
    def get(self):
        """
        Get user's authentication history
        ---
        tags:
          - User
        responses:
          200:
            description: Authentication history has been gotten
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
        """
        user_id: str = get_jwt_identity()['identifier']
        data = parser.parse_args()
        try:
            if data['page_number']:
                history = AuthHistory.return_all(user_id, int(data['page_number']))
            else:
                history = AuthHistory.return_all(user_id, 1)
        except exceptions.NotFound:
            return {'message': PAGE_NOT_FOUND}, HTTPStatus.NOT_FOUND

        if not history:
            return \
                {'message': AUTH_HISTORY_NEX.format(user_id)}
        return history, HTTPStatus.OK

    @is_admin_permissions()
    def delete(self):
        """
        Delete user's authentication history
        ---
        tags:
          - User
        responses:
          200:
            description: Authentication history has been gotten
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
        """

        return AuthHistory.delete_all(), HTTPStatus.OK


class ResetPassword:
    pass
