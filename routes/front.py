from flask import Blueprint, render_template

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
    # we should also send user_id
    fake_user = {
        "name": "عمر حسام",
        "bio": "اهلا انا عمر انا مطور مواقع مستقل و طالب ثانوي عام",
        "city": "الإسكندرية",
        "street": "محرم بك",
        "friends": 15,
        "gender": "ذكر",
        "whatsapp_phone": "01146641222",
        "facebook_link": "https://www.facebook.com/omarhossam160",
        "streak": 5,
        "xp": 1204,
        "rank": 8,
        "last_bill_cost": 320
    }
    
    return render_template('profile.html', show_user_nav=True, user=fake_user)

@front_bp.route('/api/hello', methods=['GET'])
def hello():
    return '<div>تم احضار البيانات بنجاح 🎉</div>'

@front_bp.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@front_bp.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

#@front_bp.route('/building-type/<int:user_id>')
#def building_type(user_id):
 #   return render_template('building_type.html', user_id=user_id)


