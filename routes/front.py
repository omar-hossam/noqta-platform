from flask import Blueprint, render_template

front_bp = Blueprint('front', __name__)

@front_bp.route('/', methods=['GET'])
def home():
    return render_template('index.html', is_home_page=True)

@front_bp.route('/api/hello', methods=['GET'])
def hello():
    return '<div>تم احضار البيانات بنجاح 🎉</div>'

@front_bp.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@front_bp.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')
