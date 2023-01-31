from ..viewsets import (change_password, get_auth_history, login, logout,
                        protected, registration, token_refresh, users)
from . import api_bp_auth

api_bp_auth.add_resource(registration.UserRegistration, '/registration')
api_bp_auth.add_resource(login.UserLogin, '/login')
api_bp_auth.add_resource(logout.UserLogoutAccess, '/logout')
api_bp_auth.add_resource(token_refresh.TokenRefresh, '/token/refresh')
api_bp_auth.add_resource(users.AllUsers, '/users')
api_bp_auth.add_resource(protected.SecretResource, '/protected')
api_bp_auth.add_resource(change_password.ChangePassword, '/update/password')
api_bp_auth.add_resource(get_auth_history.GetAuthHistory, '/auth/history')
