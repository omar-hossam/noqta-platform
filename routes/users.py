from flask import Blueprint, jsonify, request, redirect, url_for, make_response
from utils.db import get_db, new_profile_id
from utils.auth import hash_password, verify_password, validate_email_address

users_bp = Blueprint('users', __name__)

@users_bp.route('/register', methods=['POST'])
def register():    
    profile_id = new_profile_id()
    
    name = request.form.get('name').strip()
    if not name:
        return jsonify({'error': 'Name required'}), 400
    
    is_valid_email = validate_email_address(request.form.get('email').strip())
    if not is_valid_email:
        return jsonify({'error': 'Invalid email format'}), 400
    
    email = request.form.get('email').strip()
    
    gender = request.form.get('gender').strip()
    if not gender:
        return jsonify({'error': 'Gender required'}), 400
        
    city = request.form.get('city').strip()
    if not city:
        return jsonify({'error': 'City required'}), 400
        
    street = request.form.get('street').strip()
    if not street:
        return jsonify({'error': 'Street required'}), 400
    
    password = request.form.get('password').strip()
    if not password or len(password) < 3 or len(password) > 30:
        return jsonify({'error': 'Password must be 3-30 characters'}), 400
    
    hashed = hash_password(password)
     
    db = get_db()
    db.execute('INSERT INTO users (profile_id, name, email, gender, city, street, password_hash, xp, streak) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (profile_id, name, email, gender, city, street, hashed, 0, 0))
    
    db.commit()
    
    user_id = db.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()[0]
    
    db.close()
    
    redirect_url = url_for('front.building_type', user_id=user_id)
    response = make_response()
    response.headers['HX-Redirect'] = redirect_url
    
    return response

@users_bp.route('/login', methods=['POST'])
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

@users_bp.route('/<int:user_id>/building-type', methods=['POST'])
def building_type(user_id):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    
    if not request.form.get('building-type'):
        return jsonify({'error': 'Building type required'}), 400
    
    db.execute('UPDATE users SET building_type = ? WHERE id = ?', (request.form.get('building-type'), user_id))
    
    db.commit()
    db.close()
    
    redirect_url = url_for('front.home')
    response = make_response()
    response.headers['HX-Redirect'] = redirect_url
    
    return response

@users_bp.route('/get-all', methods=['GET'])
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
    
