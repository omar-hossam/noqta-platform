from flask import Blueprint, jsonify, request, redirect, url_for, make_response, session


shared_bp = Blueprint('shared', __name__)


"""
++++++++++++++++++
==================
    SHARED       |
==================
++++++++++++++++++
"""    


@shared_bp.route('/api/logout', methods=['GET'])
def logout():
    session.clear()
    redirect_url = url_for('front.home')
    response = make_response()
    response.headers['HX-Redirect'] = redirect_url
    return response


@shared_bp.route('/api/admin/login', methods=['POST'], endpoint='admin_login')
def admin_login():
    db = get_db()
    
    form_username = request.form.get('username').strip()
    form_password = request.form.get('password').strip()

    admin = db.execute('SELECT * FROM admins WHERE username = ?', (form_username,)).fetchone()
    db.close()
    
    if admin and check_password_hash(admin['password_hash'], form_password):
        session.clear()
        session['admin_id'] = admin['id']
        redirect_url = url_for('front.admin')
        response = make_response()
        response.headers['HX-Redirect'] = redirect_url
        
        return response
