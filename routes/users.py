from flask import Blueprint, jsonify, request
from utils.db import get_db, new_profile_id
from utils.auth import hash_password, verify_password, validate_email_address

users_bp = Blueprint('users', __name__)

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    
    profile_id = new_profile_id()
    
    name = data['name'].strip()
    if not name:
        return jsonify({'error': 'Name required'}), 400
    
    email = validate_email_address(data['email'].strip())
    if not email:
        return jsonify({'error': 'Invalid email format'}), 400
    
    gender = data['gender'].strip()
    if not gender:
        return jsonify({'error': 'Gender required'}), 400
        
    city = data['city'].strip()
    if not city:
        return jsonify({'error': 'City required'}), 400
        
    street = data['street'].strip()
    if not street:
        return jsonify({'error': 'Street required'}), 400
    
    password = data['password'].strip()
    if not password or len(password) < 3 or len(password) > 30:
        return jsonify({'error': 'Password must be 3-30 characters'}), 400
    
    hashed = hash_password(password)
     
    
    db = get_db()
    db.execute('INSERT INTO users (profile_id, name, email, gender, city, street, password_hash, xp, streak) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (profile_id, name, email, gender, city, street, hashed, 0, 0))
    
    db.commit()
    db.close()
    return jsonify({'message': 'user created'}), 201

@users_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    db = get_db()
    
    user = db.execute('SELECT * FROM users WHERE email = ?', (data['email'])).fetchone()
    db.close()
    
    if user and verify_password(data['password'], user['password']):
        return jsonify({'message': 'login success', 'user_id': user['id']})
    
    return jsonify({'message': 'Invalid credentials'}), 401

@users_bp.route('/<int:user_id>/building-type', methods=['POST'])
def building_type(user_id):
    db = get_db()
    data = request.json
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    
    if not property_type:
        return jsonify({'error': 'Building type required'}), 400
    
    db.execute('UPDATE users SET building_type = ? WHERE id = ?', (data['building-type'], user_id))
    
    db.commit()
    db.close()
    return jsonify({'message': 'Building type updated'}), 200
