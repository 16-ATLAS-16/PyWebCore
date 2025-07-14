from flask import Blueprint, render_template, flash, url_for, redirect, session
from core.sessions import GLOBAL_SESSIONMANAGER as sessions

bp = Blueprint('home', __name__, template_folder='../templates')
bp.navbar_visible = True
bp.navbar_category = 'test'

@bp.route('/')
def home():
    # experimenting with enforcing sessions for future middleware, this likely won't stick around
    if sessions.ensureSession():
        return sessions.ensureSession()
    value = {}
    if 'sid' not in session.keys():
        value['noSess'] = True
    return render_template('index.html', value=value)

@bp.route('/success')
def success():
    # similarly here, experimenting with session creation 
    if 'sid' not in session.keys():
        session['sid'] = str(sessions.createSession().SID)
    flash('success!', 'success')
    return redirect('/')

@bp.route('/error')
def error():
    flash('error!', 'danger')
    return redirect('/')

@bp.route('/index')
def index():
    return redirect('/')