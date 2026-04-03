from flask import Blueprint, jsonify, request, redirect, url_for, make_response, session
from utils.db import get_db, new_profile_id
from werkzeug.security import generate_password_hash, check_password_hash
from utils.form import validate_email_address


apis_bp = Blueprint('apis', __name__)


@apis_bp.route('/api/users/register', methods=['POST'])
def register():    
    profile_id = new_profile_id()
    db = get_db()
    
    name = request.form.get('name').strip()
    email = request.form.get('email').strip()
    gender = request.form.get('gender').strip()
    city = request.form.get('city').strip()
    street = request.form.get('street').strip()
    password = request.form.get('password').strip()

    hashed = generate_password_hash(password)
    
    db.execute('INSERT INTO users (profile_id, name, email, gender, city, street, password_hash, xp, streak, whatsapp_number, facebook_link, bio) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (profile_id, name, email, gender, city, street, hashed, 0, 0, '', '', ''))
    
    print("before commit")
    
    db.commit()
    
    print("done")
    
    user_id = db.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()[0]
    
    db.close()
    
    session['user_id'] = user_id
    
    redirect_url = url_for('front.settings')
    response = make_response()
    response.headers['HX-Redirect'] = redirect_url
    
    return response
    

@apis_bp.route('/api/users/<int:user_id>/update-settings', methods=['POST'])
def update_settings(user_id):
    db = get_db()
    bio = request.form.get('bio')
    wp_number = request.form.get('whatsapp-number')
    fb_link = request.form.get('facebook-link')
    
    db.execute('UPDATE users SET bio = ?, whatsapp_number = ?, facebook_link = ? WHERE id = ?', (bio, wp_number, fb_link, user_id,))
    
    db.commit()
    db.close()
    
    redirect_url = url_for('front.profile')
    response = make_response()
    response.headers['HX-Redirect'] = redirect_url
    return response


@apis_bp.route('/api/users/login', methods=['POST'])
def login():
    try:
        db = get_db()
        
        form_email = request.form.get('email').strip()
        if not form_email:
            return '<div>Email required!</div>' # change input border color to red when warning!
        
        form_password = request.form.get('password').strip()
        if not form_password:
            return '<div>Password required!</div>'
        
        user = db.execute('SELECT * FROM users WHERE email = ?', (form_email,)).fetchone()
        db.close()
        
        if user and verify_password(form_password, user['password']):
            return jsonify({'message': 'login success', 'user_id': user['id']})
        
        return jsonify({'message': 'Invalid credentials'}), 401
    except:
        return '<div>Something went wrong.</div>'


@apis_bp.route('/api/users/<int:user_id>/friends', methods=['GET'])
def get_friends(user_id):
    db = get_db()
    friend_ids = db.execute('SELECT friend_id FROM friends WHERE user_id = ?', (user_id,)).fetchall()
    
    
    friend_ids = [row['friend_id'] for row in friend_ids]  # list of friend IDs
    
    html_code = ""
    user_icon = url_for('static', filename='icons/user-circle.svg')
    plus_icon = url_for('static', filename='icons/plus.svg')
    
    for friend_id in friend_ids:
        friend_name = db.execute('SELECT name FROM users WHERE id = ?', (friend_id,)).fetchone()
        html_code += f"""<li>
            <div>
                <img src="{user_icon}" alt="user icon" style="width: 2rem;">
                {friend_name}
            </div>
            <button>
                إضافة صديق <img src="{plus_icon}" alt="plus icon">
            </button>
        </li>"""
     
    db.close()
    
    return html_code


@apis_bp.route('/api/users/get-all', methods=['GET'])
def get_all():
    try:
        db = get_db()
        users = db.execute('SELECT * FROM users').fetchall()
        db.close()
        users_list = []
        
        for user in users:
            users_list.append(dict(user))
        
        return jsonify({
            'users': users_list,
            'count': len(users_list)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@apis_bp.route('/api/collector', methods=['GET'], endpoint='get_collector')
def get_collector():
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
        
        session['collector_id'] = collector['id']
        redirect_url = url_for('front.collector')
        response = make_response()
        response.headers['HX-Redirect'] = redirect_url
        return response
    
    return 'بيانات إدخال خاطئة'


@apis_bp.route('/api/collector', methods=['POST'], endpoint='post_collector')
def post_collector():
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


@apis_bp.route('/api/new-bill/<int:profile_id>', methods=['POST'])
def new_bill(profile_id):
    from datetime import datetime
    # get profile_id 
    # insert the *bill_cost + user_id + collector_id* to monthly bills
    profile_id = request.form.get('profile_id').strip()
    bill_cost = request.form.get('bill_cost').strip()
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

    return "تم إضافة الفاتورة بنجاح!"
