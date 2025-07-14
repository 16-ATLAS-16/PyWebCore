# A basic user class
from ..role_manager import GLOBAL_ROLEMANAGER as RoleManager
from ..database import GLOBAL_CLIENT as db
from .role import Role
from typing_extensions import Self
import datetime, re

class User:

    ID: str
    firstName: str
    lastName: str
    userName: str
    email: str
    roles: list[Role] = []

    def __init__(self, id: str, firstName: str, lastName: str, userName: str = 'Default User', email: str = 'default@email.address', roles: list[str] | list[int] = [], **kwargs):
        self.ID = id
        self.firstName = firstName
        self.lastName = lastName
        self.userName = userName
        self.email = email

        for role in roles:
            self.add_role(role)

    def get_json(self) -> dict:
        """
        Returns a JSON representation of this object.
        """

        return {
            "id": self.ID,
            "firstname": self.firstName,
            "lastname": self.lastName,
            "displayname": self.userName,
            "email": self.email
        }

    def validate(self) -> bool:
        """
        A function used to validate the data assigned to this user object by pulling related data from the db.
        If existing matches are found, data validation is carried out.
        Returns bool for success.
        """

        fail: int = 0
            
        # Ensure name fields still match required formats.
        if type(self.firstName) != str or type(self.lastName) != str:
            fail = 1
            print('First or last name is not a string.')

        elif not self.firstName.isalpha() or not self.lastName.isalpha():
            # Name must be alphabetic characters only.
            fail = 1
            print('Contains non-alphabetic characters.')
        
        # Next, we ensure the display name is something relatively tolerable.
        if not self.userName.isalnum():
            fail = 1
            print('Not alphanum!')
        
        # Roles up next! We must ensure they're all valid still!
        for role in self.roles:
            if type(role) != Role and type(role) != str:
                fail = 1
                print(f'{role} is not a valid role.')

            if type(role) == str:
                role = RoleManager.find_role(role)

            if not role.validate():
                fail = 1
                self.roles.remove(role)
                print(f'{role} failed validation.')

        # Last but not least, the email! 
        pattern = (r"^(?!\.)(?!.*\.\.)[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"r"@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$")
        if re.match(pattern, self.email) is None:
            fail = 1
            print('Invalid email.')

        return not fail

    def add_role(self, role: Role | str) -> bool:
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
    
    def fetch_roles(self) -> bool:
        """
        Fetches roles from the database for this user.
        Returns boolean for success indication.
        """
        try:
            response = (
                db
                .schema('public')
                .table('user_roles')
                .select('role_id')
                .eq('id', self.ID)
                .execute()
            )

        except:
            print("DB IS OFFLINE!")
            return 0

        if response.data:
            for role in response['data']:
                self.add_role(role['role_id']) if len(response['data']) > 0 else 'null'

            return 1
        
        return 0
    
    def has_role(self, role: str | int | Role) -> bool:
        if type(role) == str or type(role) == int:
            role = RoleManager.find_role(role)

        return role in self.roles
    
    def find_by_uuid(self, uuid: str) -> list[Self]:
        response: dict = (
            db
            .schema('public')
            .table('users')
            .select('*')
            .eq('id', uuid)
        )

        if 'data' in response.keys():
            return [
                User(
                    id = uData['id'],
                    firstName = uData['firstName'],
                    lastName = uData['lastName'],
                    userName = uData['displayName'],
                    email = uData['email']
                ) for uData in response['data']
            ]
        
    def update(self, **kwargs):
        if 'name' in kwargs:
            self.firstName = kwargs['name'].split(' ')[0]
            self.lastName = kwargs['name'].split(' ')[1]

        if 'username' in kwargs:
            self.userName = kwargs['username']

        if 'email' in kwargs:
            self.email = kwargs['email']

    def updateDB(self):

        if self.validate():
            resp = (
                db
                .schema('public')
                .table('users')
                .update(self.get_json())
                .eq('id', self.ID)
                .execute()
            )

            if not resp.data:
                raise Exception("No such user found in DB.")
