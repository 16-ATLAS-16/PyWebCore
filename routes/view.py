from flask import Blueprint, render_template, request, session
from core.sessions import GLOBAL_SESSIONMANAGER as sessions

bp = Blueprint('view', __name__, url_prefix='/view', template_folder='../templates')
bp.navbar_visible = True
bp.navbar_category = 'test'

@bp.before_request
def middleware():
    print("Middleware!", request.url)
    sessions.ensureSession()


@bp.route('/')
def home():
    return "<p>view!</p>"

