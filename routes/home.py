from flask import Blueprint, render_template, flash, url_for, redirect

bp = Blueprint('home', __name__, template_folder='../templates')
bp.navbar_visible = True
bp.navbar_category = 'test'

@bp.route('/')
def home():
    return render_template('index.html')

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