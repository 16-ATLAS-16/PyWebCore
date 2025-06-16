# This model is for use in non-flask contexts of code execution, i.e. navigation and role manager
from typing_extensions import Self

class Route:

    NAME: str
    URL_PART: str # immutable.
    PARENT_ROUTE: Self

    def __init__(self, name: str, url_part: str = None, parent_route: str = None):  
        self.NAME = name
        self.URL_PART = '/' + url_part if url_part is not None else '/'
        self.PARENT_ROUTE = parent_route
    
    def get_full_path(self) -> str:
        final_path: str = ''
        if self.PARENT_ROUTE != None:
            final_path += self.PARENT_ROUTE.get_full_path()
        final_path += self.URL_PART
        return final_path
    
    def get_navbar_representation(self) -> tuple[str, str]:
        return (self.NAME, f'{self.NAME}.home')