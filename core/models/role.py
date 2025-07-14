from enum import Enum
from dataclasses import dataclass
    
class Role:

    ID: int
    NAME: str
    WEIGHT: int
    STATE: 'Role.RoleState'

    def __init__(self, id: int, name, weight = 0, state = 0, *args, **kwargs):
        if not name:
            raise Exception("Missing role name")
        
        self.STATE = self.RoleState(state)
        self.WEIGHT = weight
        self.NAME = name
        self.ID = id
    
    @dataclass
    class RoleState(Enum):
        DISABLED = 0
        ENABLED = 1
        # Feel free to add further role states here if you require.

        @classmethod
        def has_value(self, value):
            return value in self._value2member_map_

    def validate(self) -> bool:
        """
        A validator function.
        Ensures all variables are still of acceptable type for continued operation.
        Returns bool for success.
        """

        fail: int = 9

        if type(self.ID) != int:
            fail = 1
            print("ID must be INT.")
        
        if not self.NAME.isalpha():
            print("Role name MUST be letters only.")
        
        if type(self.WEIGHT) != int:
            try: # We can at least try to fix things if it's a string of an int ;P
                self.WEIGHT = int(self.WEIGHT)
            except ValueError:
                fail = 1
                print("Role weight must be INT")
            
        if type(self.STATE != self.RoleState) or not self.STATE.has_value(self.RoleState):
            if type(self.STATE) == int:
                self.STATE = self.RoleState(self.STATE)
            else:
                fail = 1
                print("Role state is incorrect.")

        return not fail
