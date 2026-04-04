from flask import Flask, jsonify, request, session
from flask_cors import CORS
from utils.db import init_db, get_db
from routes.front import front_bp
from routes.apis.shared import shared_bp
from routes.apis.user import user_bp
from routes.apis.collector import collector_bp


app = Flask(__name__)
app.secret_key = 'super-secret-ultra-safe-key'
CORS(app, supports_credentials=True) 


app.register_blueprint(front_bp)
app.register_blueprint(user_bp)
app.register_blueprint(collector_bp)
app.register_blueprint(shared_bp)


@app.before_request
def before_every_request():
    init_db()
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    num_of_users = cursor.fetchone()[0]
    
    if num_of_users == 0:
        session.pop('user_id', None)
    
    cursor.execute("SELECT COUNT(*) FROM collectors")
    num_of_collectors = cursor.fetchone()[0]
    
    if num_of_collectors == 0:
        session.pop('collector_id', None)
    
    cursor.execute("SELECT COUNT(*) FROM admins")
    num_of_admins = cursor.fetchone()[0]
    
    if num_of_admins == 0:
        session.pop('admin_id', None)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
