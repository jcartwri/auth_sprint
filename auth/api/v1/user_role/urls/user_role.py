from ..viewsets import add_user_role, delete_user_role, show_user_role
from . import api_bp_user_role

api_bp_user_role.add_resource(add_user_role.CreateUserRole, "/add_user_role")
api_bp_user_role.add_resource(delete_user_role.DeleteUserRole, "/delete_user_role")
api_bp_user_role.add_resource(delete_user_role.DeleteAllUserRoles, "/delete_user_role/all")
api_bp_user_role.add_resource(show_user_role.ShowUserRole, "/show_user_role")
