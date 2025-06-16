from .models.route import Route
from .models.category import Category
from flask import Blueprint
import os

class Navigations:

    role_restrictions: list[dict] = []
    routes: list[Route] = []
    navbarVisibleRoutes: list[Route] = []
    navbarCategories: list[tuple[str, list[Route]]] = []

    def __init__(self, role_restrictions : list = None, routes: list[Blueprint] = [], **configs):
        self.role_restrictions = self.parse_restrictions(role_restrictions) if role_restrictions else []
        if configs.get('role_location'):
            import configparser
            with configparser.ConfigParser() as settings:
                try:
                    settings.read(configs['role_location'])
                except Exception as e:
                    raise Exception(e)
                
    @property
    def total_navigators(self) -> int:
        return len(self.routes)

    def parse_restrictions(self, rules):
        """
            A function for parsing fine-tuning and control rulesets for what navigations are shown.
            For example, the ruleset:
                {route: 'any', role: 'admin', show: 'role_only'}
            Will only show navigations with the 'admin' visibility and 'all' visibility on all routes.

            Restrictions can be any of the following:

                role_only    => shows navigation for 'all' and '<role>'
                highest_role => shows navigation for 'all', and all roles below and equal to highest role (default)
                all          => ignores roles and shows all items
                none         => shows none. (useful for disabling or hiding elements relying on this class)

            Specifying 'route' can limit such restrictions to given route/navigators only.
        """

        for rule in rules:
            self.role_restrictions.append({
                'route': rule.route | 'any',
                'role': rule.role | 'any',
                'show': rule.show | 'highest_role'
            })

    def find_route_by_name(self, route_name: str = None) -> Route | None:
        """
        Finds a route object by name.
        Returns: Route or None.
        """
        for route in self.routes:
            if route.NAME == route_name:
                return route
            
        if len(route_name) == 0:
            return self.get_home_route()
            
        return None
    
    def get_child_routes(self, route_name: str = None) -> list[Route]:
        """
        Finds all "child" routes of a given route and returns them.
        Returns: list of Routes (may be empty)
        """
        return [route for route in self.routes if self.find_route_by_name(route_name).URL_PART in route.get_full_path() and route.NAME != route_name]

    def register_routes(self, blueprints: list[Blueprint] = []) -> None:
        """
        Registers a list of routes, resolving their parent routes in the process.
        """

        routeBuffer: list[tuple[int, Blueprint]] = [(len(list(filter(lambda x: x.strip(), route.url_prefix.split('/') if route.url_prefix else ''))), route) for route in blueprints]
        routeBuffer.sort()

        for parentCount, route in routeBuffer:

            parentRoute = self.find_route_by_name(route.url_prefix.split('/')[-2]) if parentCount else self.get_home_route()
            prefix = route.url_prefix.split('/')[-1] if parentCount else ''

            self.routes.append(Route(route.name, prefix, parentRoute))
            if hasattr(route, 'navbar_visible'):
                self.navbarVisibleRoutes.append(self.routes[-1])

            route.url_prefix = '/' + prefix
            print(f"Registered route: {route.name} with parent {parentRoute.NAME if parentRoute else 'None'}")

    def import_routes_from(self, path: str = None) -> list[Blueprint] | None:

        """
        Imports routes from any given directory.
        Routes MUST be .py files.
        """

        if path:
            routeBuffer: list[Blueprint] = []
            for route in os.listdir(path):
                if route.endswith('.py'):
                    routeName = route.strip('.py')
                    regCmd = f'from routes.{routeName} import bp as {routeName}_bp\nrouteBuffer.append({routeName}_bp)'
                    exec(regCmd)

            self.register_routes(routeBuffer)

            return routeBuffer
        
        return None
    
    def get_home_route(self) -> Route | None:
        """
        A method that finds and returns the route bound to '/'
        """

        for route in self.routes:
            if route.URL_PART == '/':
                return route
            
        return None
    
    def find_route_category(self, route: Route) -> Category | None:
        pass
    
    def get_navbar(self) -> list[tuple[str, str]]:
        """
        Returns navbar items.
        Future improvements will see this function return differently based on session data.
        """
        return ([route.get_navbar_representation() for route in self.navbarVisibleRoutes if not self.find_route_category(route)])

GLOBAL_NAVMANAGER = Navigations()