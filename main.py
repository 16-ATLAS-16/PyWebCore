from flask import Flask, send_from_directory, Blueprint, session
import os, configparser
import core.navigation as Navigation
from core.role_manager import RoleManager
from core.models.user import User

config = configparser.ConfigParser()
config.read(['main.config'])

app = Flask(__name__, static_folder='./static')
app.secret_key = config['app_config']['secret']

blueprints = Navigation.GLOBAL_NAVMANAGER.import_routes_from('./routes')
for bp in blueprints:
    app.register_blueprint(bp)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.context_processor
def appNavManager():
    return {'nav' : Navigation.GLOBAL_NAVMANAGER}


app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.run(
    host=config['app_config']['host'],
    port=config['app_config']['port']
)