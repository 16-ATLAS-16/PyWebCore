from enum import Enum
    
class Role:

    ID: int
    NAME: str
    WEIGHT: int
    STATE: Enum

    def __init__(self, id, name, weight = 0, state = 0, *args, **kwargs):
        if not name or not weight or not state:
            raise Exception("Missing role name")
        
        self.STATE = self.RoleState(state)
        self.WEIGHT = weight
        self.NAME = name
    
    class RoleState(Enum):
        DISABLED = 0
        ENABLED = 1
        # Feel free to add further role states here if you require.
