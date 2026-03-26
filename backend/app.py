from flask import Flask, jsonify, request, session
from flask_cors import CORS
from src.brain import init_db, get_db, DB_PATH, new_profile_id

app = Flask(__name__)
app.secret_key = 'super-secret-ultra-safe-key'
CORS(app, supports_credentials=True) 

init_db()

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({ "msg": "HI!", "Random1": new_profile_id(), "Random2": new_profile_id(), "Random3": new_profile_id(), "Random4": new_profile_id(), "Random5": new_profile_id() })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
