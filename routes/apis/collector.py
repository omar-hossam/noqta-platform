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
    
    saved_hash_password = saved_hash_password['password_hash'] 
    
    if check_password_hash(saved_hash_password, password):
        collector = db.execute('SELECT * FROM collectors WHERE code = ?', (code,)).fetchone()
        
        session.clear()
        session['collector_id'] = collector['id']
        redirect_url = url_for('front.collector')
        response = make_response("Done")
        response.headers['HX-Redirect'] = redirect_url
        return response
    
    return 'Invalid Credintals!'

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


@collector_bp.route('/api/collector/<int:collector_id>/delete', methods=['POST'], endpoint='user_delete')
def user_delete(collector_id):
    db = get_db()
    
    db.execute("DELETE FROM collectors WHERE id = ?", (collector_id,)).fetchone()
    db.commit()
    db.close()
    
    try:
        if session['collector_id']:
            session.pop('collector_id', None)
    except:
        print("")
    
    response = make_response()
    
    try:
        if session['admin_id']:
            response = make_response('تم حذف المحصل بنجاح!')
            response.headers['HX-Trigger'] = 'contentUpdated' 
    except KeyError:
        redirect_url = url_for('front.home')
        response.headers['HX-Redirect'] = redirect_url
    
    return response
    

@collector_bp.route('/api/collector/new-bill', methods=['POST'])
def new_bill():
    from datetime import datetime
    # get profile_id 
    # insert the *bill_cost + user_id + collector_id* to monthly bills
    profile_id = request.form.get('profile-id').strip()
    bill_cost = request.form.get('bill-cost').strip()
    collector_id = session['collector_id'] 
     
    db = get_db()

    rows = db.execute('SELECT id, name FROM users WHERE profile_id = ?', (profile_id,)).fetchone()

    now = datetime.now() 
    month = now.month
    year = now.year

    db.execute('INSERT INTO bills (user_id, collector_id, cost, month, year) VALUES (?, ?, ?, ?, ?)', (rows['id'], collector_id, bill_cost, month, year))

    db.commit()
    db.close()

    html_code = f"<article class='pico-background-green-500'>تم إضافة الفاتورة إلي {rows['name']} بنجاح!</article>"

    response = make_response(html_code)
    response.headers['HX-Trigger'] = 'contentUpdated'  # Trigger client event
    return response 


@collector_bp.route('/api/collector/<int:collector_id>/bills', methods=['GET'], endpoint="get_collector_bills")
def get_collector_bills(collector_id):
    db = get_db()
    query = 'SELECT * FROM bills WHERE collector_id = ? ORDER BY year DESC, month DESC'
    bills = db.execute(query, (collector_id,)).fetchall()
    
    response = make_response()
    current_page = request.referrer

    if current_page.endswith("/admin/table/collectors"):
        response = make_response(f'{len(bills)}')
        
    else:
        html_code = ""
        
        for bill in bills:
            user_row = db.execute("SELECT profile_id FROM users WHERE id = ?", (bill['user_id'],)).fetchone()
            user_profile_id = user_row['profile_id']
            
            html_code += f"""
                <tr class="user-row">
                    <th scope="row"><a href="/profile/{user_profile_id}" target="_blank">{user_profile_id}</a></th>
                    <td>{bill['issued_at']}</td>
                    <td>{bill['month']}</td>
                    <td>{bill['year']}</td>
                    <td>{bill['cost']}</td>
                </tr>
            """
        response = make_response(html_code)
        
    response.headers['HX-Trigger'] = 'contentUpdated'
    db.close()
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
                
                <td class="grid">
                    <a role="button" style="background: transparent; border: 0; color: inherit; font-weight: bold;" href="/admin/table/collectors/{x['id']}" hx-get="/api/collector/{x['id']}/bills" hx-target="this" hx-swap="textContent" hx-trigger="load"></a></td>
                
                <td><button class="pico-background-red-600" style="border: 0;" hx-post="/api/collector/{x['id']}/delete">حذف</button></td>
            </tr>
        """
    
    db.close()
    
    response = make_response(html_code)
    response.headers['HX-Trigger'] = 'contentUpdated'  # Trigger client event
    return response
