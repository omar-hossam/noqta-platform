from flask import Blueprint, render_template, session, redirect, send_from_directory
from utils.db import get_db
from utils.starter_todos import todos


front_bp = Blueprint('front', __name__)
    

@front_bp.route('/')
def home():
    is_logged = False
    try:
        if session['user_id']:
            is_logged = True
    except KeyError:
        is_logged = False
    
    return render_template('index.html', show_home_nav=True, is_logged=is_logged)


@front_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)


@front_bp.route('/website/pages')
def website_pages():
    return render_template('pages.html')


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
            db = get_db()
            
            user = db.execute("SELECT * FROM users WHERE id = ?", (session['user_id'],)).fetchone()
            db.close()
            
            return render_template('dashboard.html', show_user_nav=True, todos=todos, user_id=user['id'])
    except KeyError:
        return redirect('/login')


@front_bp.route('/ranking')
def ranking():
    try:
        if session['user_id']:
            return render_template('ranking.html', show_user_nav=True)
        elif session['admin_id'] or session['collector_id']:
            return render_template('ranking.html', show_home_nav=True)
    except KeyError:
        return redirect('/login')


def get_chart_data(db, user_id):
    query = 'SELECT cost, month FROM bills WHERE user_id = ? ORDER BY month ASC LIMIT 6'
    bills = db.execute(query, (user_id,)).fetchall()
    
    data = [0, 0, 0, 0, 0, 0]
    
    # April -> September
    for bill in bills:
        if bill['month'] == 4:
            data[0] = bill['cost']
        elif bill['month'] == 5:
            data[1] = bill['cost']
        elif bill['month'] == 6:
            data[2] = bill['cost']
        elif bill['month'] == 7:
            data[3] = bill['cost']
        elif bill['month'] == 8:
            data[4] = bill['cost']
        elif bill['month'] == 9:
            data[5] = bill['cost']
    return data


@front_bp.route('/profile', methods=['GET'])
def profile():
    try:
        if session['user_id']: 
            db = get_db()

            user_id = session['user_id']
            user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            
            data = get_chart_data(db, user_id)
                    
            
            db.close()
            return render_template('profile.html', show_user_nav=True, user=user, data=data)
    except KeyError:
        return redirect('/login')


@front_bp.route('/social', methods=['GET'])
def social():
    try:
        if session['user_id']: 
            db = get_db()

            user = db.execute("SELECT * FROM users WHERE id = ?", (session['user_id'],)).fetchone()

            return render_template('social.html', show_user_nav=True, user=user)
    except KeyError:
        return redirect('/login')


@front_bp.route('/settings')
def settings():
    try:
        if session['user_id']:    
            db = get_db()
            user_id = session['user_id']
            user = db.execute("SELECT id, bio, whatsapp_number, facebook_link, streak, xp, profile_id, profile_photo, cover_photo FROM users WHERE id = ?", (user_id,)).fetchone()
            
            db.close()
            return render_template('settings.html', show_user_nav=True, user=user)
    except KeyError:
        return redirect('/login')


@front_bp.route('/profile/<int:profile_id>', endpoint="public_profile")
def public_profile(profile_id):
    if len(session.keys()) > 0:
        db = get_db()

        try:
            user = db.execute("SELECT * FROM users WHERE profile_id = ?", (profile_id,)).fetchone()
            
            data = get_chart_data(db, user['id'])
            
            db.close()
            
            SHOW_USER_NAV = False
            SHOW_ADMIN_NAV = False
            SHOW_COLLECTOR_NAV = False
            
            if 'user_id' in session:
                SHOW_USER_NAV = True
            elif 'collector_id' in session:
                SHOW_COLLECTOR_NAV = True
            elif 'admin_id' in session:
                SHOW_ADMIN_NAV = True
            
            return render_template('profile.html', show_user_nav=SHOW_USER_NAV, user=user, data=data, show_admin_nav=SHOW_ADMIN_NAV, show_collector_nav=SHOW_COLLECTOR_NAV)
            
        except TypeError:   
            db.close()
            return render_template('404.html')
    else:
        return redirect('/')
        
"""
++++++++++++++++++++
====================
     COLLECTOR     |
====================
++++++++++++++++++++
""" 

@front_bp.route('/collector')
def collector():
    try:
        from datetime import datetime
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        if session['collector_id']:
            return render_template('collector.html', current_month=current_month, current_year=current_year)
    except KeyError:
        return redirect('/login')


"""
++++++++++++++++
================
     ADMIN     |
================
++++++++++++++++
""" 


@front_bp.route('/admin/table/collectors', endpoint="admin_collectors")
def admin_collectors():
    #try:
        #if session['admin_id']:
    return render_template('admin/collectors.html', is_logged=True)
   # except KeyError:
        #return render_template('admin/admin.html', is_logged=False)


@front_bp.route('/admin/table/users', endpoint="admin_users")
def admin_users():
    try:
        if session['admin_id']:
            return render_template('admin/users.html', is_logged=True)
    except KeyError:
        return render_template('admin/admin.html', is_logged=False)


@front_bp.route('/admin', endpoint="admin")
def admin():
    try:
        if session['admin_id']:
            return render_template('admin/admin.html', is_logged=True)
    except KeyError:
        return render_template('admin/admin.html', is_logged=False)


@front_bp.route('/admin/table/collectors/<int:collector_id>')
def collector_bills(collector_id):
    try:
        if session['admin_id']:
            db = get_db()
            p = db.execute('SELECT * FROM collectors WHERE id = ?', (collector_id,)).fetchone()
            
            db.close()
            
            return render_template('admin/collector.html', is_logged=True, p=p)
    except KeyError:
        return render_template('admin/admin.html', is_logged=False)
    
