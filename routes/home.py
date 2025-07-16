from flask import Blueprint, render_template, flash, request, url_for, redirect, session
from core.sessions import GLOBAL_SESSIONMANAGER as sessions

bp = Blueprint('home', __name__, template_folder='../templates')
bp.navbar_visible = True
bp.navbar_category = 'test'

@bp.before_request
def middleware():
    print("Middleware!", request)
    sessions.ensureSession()

@bp.route('/')
def home():
    return render_template('index.html', value={})

@bp.route('/success')
def success():
    flash('success!', 'success')
    return redirect('/')

@bp.route('/error')
def error():
    flash('error!', 'danger')
    return redirect('/')

@bp.route('/index')
def index():
    return redirect('/')