from flask import Blueprint, jsonify, request, redirect, url_for, make_response, session
from utils.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash


collector_bp = Blueprint('collector', __name__)


"""
++++++++++++++++++++++
======================
    COLLECTORS       |
======================
++++++++++++++++++++++
"""    
    

@collector_bp.route('/api/collector/login', methods=['POST'], endpoint='collector_login')
def collector_login():
    db = get_db()
    
    code = request.form.get('code').strip()
    password = request.form.get('password').strip()
    
    saved_hash_password = db.execute('SELECT password_hash FROM collectors WHERE code = ?', (code,)).fetchone()
    
    saved_hash_password = saved_hash_password[0] if saved_hash_password else None
    
    if not saved_hash_password:
        db.close()
        return 'بيانات إدخال خاطئة'
    
    if check_password_hash(saved_hash_password, password):
        collector = db.execute('SELECT * FROM collectors WHERE code = ?', (code,)).fetchone()
        
        session.clear()
        session['collector_id'] = collector['id']
        redirect_url = url_for('front.collector')
        response = make_response()
        response.headers['HX-Redirect'] = redirect_url
        return response
    
    return 'بيانات إدخال خاطئة'


@collector_bp.route('/api/collector/register', methods=['POST'], endpoint='collector_register')
def collector_register():
    db = get_db()
    
    name = request.form.get('name').strip()
    code = request.form.get('code').strip()
    password = request.form.get('password').strip()
    gender = request.form.get('gender').strip()
    city = request.form.get('city').strip()
    street = request.form.get('street').strip()
    province = request.form.get('province').strip()
    
    password_hash = generate_password_hash(password)
    
    db.execute('INSERT INTO collectors (name, code, password_hash, city, gender, street, province) VALUES (?, ?, ?, ?, ?, ?, ?)', (name, code, password_hash, gender, city, street, province))
    
    db.commit()
    db.close()
    
    return "تم إضافة المحصل بنجاح!"


@collector_bp.route('/api/collector/new-bill', methods=['POST'])
def new_bill():
    from datetime import datetime
    # get profile_id 
    # insert the *bill_cost + user_id + collector_id* to monthly bills
    profile_id = request.form.get('profile-id').strip()
    bill_cost = request.form.get('bill-cost').strip()
    collector_id = session['collector_id'] 
     
    db = get_db()

    user_id = db.execute('SELECT id FROM users WHERE profile_id = ?', (profile_id,)).fetchone()
    user_id = user_id[0] if user_id else None

    if not user_id:
      return "Error!", 400

    now = datetime.now() 
    month = now.month
    year = now.year

    db.execute('INSERT INTO bills (user_id, collector_id, cost, month, year) VALUES (?, ?, ?, ?, ?)', (user_id, collector_id, bill_cost, month, year))

    db.commit()
    db.close()

    return f"<article class='pico-background-green-500'>تم إضافة الفاتورة إلي {name} بنجاح!</article>"
