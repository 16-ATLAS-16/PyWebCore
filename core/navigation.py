class Navigations:

    role_restrictions = []
    routes = []
    total_navigators = 0

    def __init__(self, role_restrictions : list = None, **configs):
        self.role_restrictions = self.parse_restrictions(role_restrictions)
        if configs['role_location']:
            import configparser
            conf = configparser()


    def parse_restrictions(self, rules):
        """
            A function for parsing fine-tuning and control rulesets for what navigations are shown.
            For example, the ruleset:
                {route: 'any', role: 'admin', show: 'role_only'}
            Will only show navigations with the 'admin' visibility and 'all' visibility.

            Restrictions can be any of the following:

                role_only    => shows navigation for 'all' and '<role>'
                highest_role => shows navigation for 'all', and all roles below and equal to highest role (default)
                all          => ignores roles and shows all items
                none         => shows none. (useful for disabling or hiding elements relying on this class)

            Specifying 'route' can limit such restrictions to given route/navigators only.
        """

        for rule in rules:

            self.role_restrictions.append()

class Navigator:
    def __init__(self, name, uri, base_path=None, visible_to=None):
        self.name = name
        self.base_path = base_path
        self.uri = uri
        self.visible_to = ['all'] if not visible_to else visible_to

    @property
    def name(self):
        return self.name
    
    @property
    def uri(self):
        return self.uri
    
    @name.setter
    def name(self, value):
        self.name = value

    @uri.setter
    def uri(self, uri):
        self.uri = self.base_path + '/' + uri

    