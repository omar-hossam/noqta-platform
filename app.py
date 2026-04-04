from flask import Flask, jsonify, request, session
from flask_cors import CORS
from utils.db import init_db
from routes.front import front_bp
from routes.apis.shared import shared_bp
from routes.apis.user import user_bp
from routes.apis.collector import collector_bp


app = Flask(__name__)
app.secret_key = 'super-secret-ultra-safe-key'
CORS(app, supports_credentials=True) 

init_db()

app.register_blueprint(front_bp)
app.register_blueprint(user_bp)
app.register_blueprint(collector_bp)
app.register_blueprint(shared_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
