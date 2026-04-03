from flask import Blueprint, render_template, session, redirect
from utils.db import get_db
from utils.starter_todos import todos


front_bp = Blueprint('front', __name__)


@front_bp.route('/')
def home():
    return render_template('index.html', show_home_nav=True)


@front_bp.route('/about')
def about():
    return render_template('about.html')


@front_bp.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@front_bp.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


@front_bp.route('/dashboard')
def dashboard():
    try:
        if session['user_id']:
            return render_template('dashboard.html', show_user_nav=True, todos=todos)
    except KeyError:
        return redirect('/login')


@front_bp.route('/profile', methods=['GET'])
def profile():
    try:
        if session['user_id']: 
            db = get_db()
            user_id = session['user_id']
            user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

            return render_template('profile.html', show_user_nav=True, user=user)
    except KeyError:
        return redirect('/login')


@front_bp.route('/settings')
def settings():
    try:
        if session['user_id']:    
            db = get_db()
            user_id = session['user_id']
            user = db.execute("SELECT id, bio, whatsapp_number, facebook_link FROM users WHERE id = ?", (user_id,)).fetchone()
            
            db.close()
            return render_template('settings.html', show_user_nav=True, user=user)
    except KeyError:
        return redirect('/login')


@front_bp.route('/collector')
def collector():
    try:
        if session['collector_id']:
            return render_template('collector.html')
    except KeyError:
        return redirect('/')
