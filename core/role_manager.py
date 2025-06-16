from .models.role import Role
from .models.route import Route

class RoleManager:

    ACTIVE_ROLES: list[Role]

    def __init__(self, *args, **kwargs):
        return
    
    def can_access_route(self, role_name: str, route: str | Route) -> bool:
        return
    
    def create_role(self, role_name: str = 'Default', role_weight: int = 0, role_state: enumerate = 0) -> None:
        """
        Creates a new role.
        """
        try:
            if role_state == Role.RoleState.ENABLED:
                self.ACTIVE_ROLES.append(Role(role_name, role_weight, role_state))
        except Exception as e:
            raise Exception(e) # if for any reason we run into issues, best to throw them.
        return
    
    def find_role(self, role_id: int = None, role_name: str = None) -> Role | None:   
        """
        Function used for finding a role by name or ID.
        """ 
        for role in self.ACTIVE_ROLES:
            if role.ID == role_id or role.NAME == role_name:
                return role
        
        return None