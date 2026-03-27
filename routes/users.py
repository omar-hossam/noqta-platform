from flask import Blueprint, jsonify, request
from utils.db import get_db

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
def get_users():
    db = get_db()
    users = db.execute('SELECT * FROM users').fetchall()
    db.close()
    return jsonify([dict(user) for user in users])

@users_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
    db.close()
    return jsonify(dict(user)) if user else ({'error': 'Not found'}, 404)
