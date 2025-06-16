from flask import Blueprint, render_template

bp = Blueprint('test', __name__, url_prefix='/test', template_folder='../templates')
bp.navbar_visible = True

@bp.route('/')
def home():
    return "<p>test!!</p>"