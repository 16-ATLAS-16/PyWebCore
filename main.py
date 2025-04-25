from flask import Flask
import os

app = Flask(__name__)
for route in os.listdir('./routes'):
    if route.endswith('.py'):
        routeName = route.strip('.py')
        regCmd = f'from routes.{routeName} import bp as {routeName}_bp\napp.register_blueprint({routeName}_bp)'
        exec(regCmd)
        print('Registered route: ', routeName)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.run()