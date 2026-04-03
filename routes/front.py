from flask import Blueprint, render_template, session, redirect
from utils.db import get_db

front_bp = Blueprint('front', __name__)

@front_bp.route('/', methods=['GET'])
def home():
    return render_template('index.html', show_home_nav=True)


@front_bp.route('/dashboard', methods=['GET'])
def dashboard():
    todos = [
        {"id": 1, "name": "خليت الدش أقل من 5 دقايق", "score": 10},
        {"id": 2, "name": "قفلت الحنفية وأنا بنظف الأسنان", "score": 10},
        {"id": 3, "name": "ريت الزرع قبل المغرب أو بعد الفجر", "score": 15},
        {"id": 4, "name": "شغلت الغسالة لما اكتملت بس", "score": 10},
        {"id": 5, "name": "صلحت حنفية كانت بتنقط لوحدها", "score": 20},
        {"id": 6, "name": "بلغت أهلى و ذكرت اصحابى بمهام انهارده", "score": 15},
        {"id": 7, "name": "سبت الأطباق تتلم شوية قبل ما أغسلها", "score": 10},
        {"id": 8, "name": "غسلت العربية بميه اقل - او بالدلو بدل الخرطوم", "score": 15},
        {"id": 9, "name": "استخدمت مية التكييف في الزرع", "score": 20},
        {"id": 10, "name": "مسحت الأرض بممسحة بدل ما أرش مية", "score": 10},
        {"id": 11, "name": "شيكت على الحنفيات كلها لو في تسريب", "score": 15},
        {"id": 12, "name": "ملّيت كاسات الميه في البيت على قد الإحتياج", "score": 10}
    ]
    
    return render_template('dashboard.html', show_user_nav=True, todos=todos)


@front_bp.route('/profile', methods=['GET'])
def profile():
    db = get_db()
    user_id = session['user_id']
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    
    return render_template('profile.html', show_user_nav=True, user=user)


@front_bp.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@front_bp.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


@front_bp.route('/settings')
def settings():
    db = get_db()
    user_id = session['user_id']
    user = db.execute("SELECT id, bio, whatsapp_number, facebook_link FROM users WHERE id = ?", (user_id,)).fetchone()
    
    db.close()
    return render_template('settings.html', show_user_nav=True, user=user)


@front_bp.route('/about')
def about():
    return render_template('about.html')


@front_bp.route('/collector')
def collector():
    try:
        if session['collector_id']:
            return render_template('collector.html')
    except KeyError:
        return redirect('/')
