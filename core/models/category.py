from .route import Route

class Category:
    """
    A simple object used to categorise and group routes.
    """

    NAME: str
    routes: list[Route]

    def __init__(self, name: str, initialRoutes: list[Route] = []):
        self.NAME = name
        self.routes = initialRoutes

    def add_route(self, route: Route) -> None:
        self.routes.append(route)

    def add_routes(self, routes: list[Route]) -> None:
        [self.add_route(route) for route in routes]

    def remove_route(self, route: Route) -> None:
        if route in self.routes:
            self.routes.remove(route)
        
    def get_navbar_routes(self) -> list[str, str]:
        return [route.get_navbar_representation() for route in self.routes]