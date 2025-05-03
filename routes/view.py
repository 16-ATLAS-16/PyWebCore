from flask import Blueprint, render_template

bp = Blueprint('view', __name__, url_prefix='/view', template_folder='../templates')

@bp.route('/')
def home():
    return "<p>view!</p>"

