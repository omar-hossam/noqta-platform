from flask import Blueprint, render_template

front_bp = Blueprint('front', __name__)

@front_bp.route('/', methods=['GET'])
def home():
    return render_template('index.html', title='Home')

@front_bp.route('/api/hello', methods=['GET'])
def hello():
    return '<div>تم احضار البيانات بنجاح 🎉</div>'
