from flask import Flask, jsonify, request, session
from flask_cors import CORS
from utils.db import init_db
from routes.users import users_bp
from routes.front import front_bp

app = Flask(__name__)
app.secret_key = 'super-secret-ultra-safe-key'
CORS(app, supports_credentials=True) 

init_db()

app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(front_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
