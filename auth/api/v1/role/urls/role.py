from ..viewsets import change, create, delete, show
from . import api_bp_role

api_bp_role.add_resource(create.CreateRole, "/role/create")
api_bp_role.add_resource(delete.DeleteRole, "/role/delete")
api_bp_role.add_resource(delete.DeleteAllRoles, "/role/delete/all")
api_bp_role.add_resource(change.ChangeRole, "/role/change")
api_bp_role.add_resource(show.ShowRoles, "/role/show")
