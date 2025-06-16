# A basic user class
from ..role_manager import RoleManager
from .role import Role
import datetime

class User:

    ID: int
    firstName: str
    lastName: str
    userName: str
    email: str
    roles: list[Role]

    def __init__(self, id: int, firstName: str, lastName: str, userName: str = 'Default User', email: str = 'default@email.address', roles: list[str] | list[int] = [], **kwargs):
        self.ID = id
        self.firstName = firstName
        self.lastName = lastName
        self.userName = userName
        self.email = email

        for role in roles:
            self.add_role(RoleManager, self, role)

    def add_role(self,  role: Role | str) -> bool:
        """
        Adds a role to this user.
        Returns: bool - whether or not the role was added to the user specified.
        """
        if type(role) == str:
            role = RoleManager.find_role(role)
            if not role:
                return 0
        if role.RoleState == 1:
            self.roles.append(role)
            return 1
        return 0

        

