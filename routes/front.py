from flask import Blueprint, render_template

front_bp = Blueprint('front', __name__)

@front_bp.route('/', methods=['GET'])
def home():
    return render_template('index.html', is_home_page=True)

@front_bp.route('/dashboard', methods=['GET'])
def dashboard():
    todos = ['hello', 'bla', 'ajksjdk']
    
    return render_template('user_home.html', is_home_page=False, is_user_logged=True, todos=todos)

@front_bp.route('/api/hello', methods=['GET'])
def hello():
    return '<div>تم احضار البيانات بنجاح 🎉</div>'

@front_bp.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@front_bp.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@front_bp.route('/building-type/<int:user_id>')
def building_type(user_id):
    return render_template('building_type.html', user_id=user_id)
