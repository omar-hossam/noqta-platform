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
    
    print('we are here!')
    
    saved_hash_password = saved_hash_password['password_hash'] 
    
    if check_password_hash(saved_hash_password, password):
        collector = db.execute('SELECT * FROM collectors WHERE code = ?', (code,)).fetchone()
        
        session.clear()
        session['collector_id'] = collector['id']
        redirect_url = url_for('front.collector')
        response = make_response()
        response.headers['HX-Redirect'] = redirect_url
        return response


@collector_bp.route('/api/collector/register', methods=['POST'], endpoint='collector_register')
def collector_register():
    db = get_db()
    
    name = request.form.get('name').strip()
    code = request.form.get('code').strip()
    password = request.form.get('password').strip()
    city = request.form.get('city').strip()
    street = request.form.get('street').strip()
    
    password_hash = generate_password_hash(password)
    
    db.execute('INSERT INTO collectors (name, code, password_hash, city, street) VALUES (?, ?, ?, ?, ?)', (name, code, password_hash, city, street))
    
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

    html_code = f"<article class='pico-background-green-500'>تم إضافة الفاتورة إلي {name} بنجاح!</article>"

    response = make_response(html_code)
    response.headers['HX-Trigger'] = 'contentUpdated'  # Trigger client event
    return response 


@collector_bp.route('/api/collectors')
def get_collectors():
    db = get_db()
    
    collectors = db.execute("SELECT * FROM collectors")
    
    html_code = ""
    
    for x in collectors:
        html_code += f"""
            <tr>
                <th scope="row">{x['name']}</th>
                <td>{x['city']}</td>
                <td>{x['street']}</td>
                <td>{x['code']}</td>
            </tr>
        """
    
    db.close()
    
    response = make_response(html_code)
    response.headers['HX-Trigger'] = 'contentUpdated'  # Trigger client event
    return response
