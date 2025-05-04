from flask import Flask, send_from_directory
import os, configparser

config = configparser.ConfigParser()
settings = config.read('main.config')

app = Flask(__name__, static_folder='./static')
app.secret_key = settings['app_config']['secret']

for route in os.listdir('./routes'):
    if route.endswith('.py'):
        routeName = route.strip('.py')
        regCmd = f'from routes.{routeName} import bp as {routeName}_bp\napp.register_blueprint({routeName}_bp)'
        exec(regCmd)
        print('Registered route: ', routeName)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.run(
    host=settings['app_config']['host'],
    port=settings['app_config']['port']
)