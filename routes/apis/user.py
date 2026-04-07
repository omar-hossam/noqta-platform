from flask import Blueprint, jsonify, request, redirect, url_for, make_response, session
from utils.db import get_db, new_profile_id
from werkzeug.security import generate_password_hash, check_password_hash
import os


user_bp = Blueprint('user', __name__)


"""
+++++++++++++++++
=================
     USER       |
=================
+++++++++++++++++
""" 


@user_bp.route('/api/user/register', methods=['POST'], endpoint="user_register")
def user_register():    
    profile_id = new_profile_id()
    db = get_db()
    
    name = request.form.get('name').strip()
    email = request.form.get('email').strip()
    gender = request.form.get('gender').strip()
    city = request.form.get('city').strip()
    city_arabic = request.form.get('city-arabic').strip()
    street = request.form.get('street').strip()
    password = request.form.get('password').strip()

    hashed = generate_password_hash(password)
    
    db.execute('INSERT INTO users (profile_id, name, email, gender, city, street, password_hash, xp, streak, whatsapp_number, facebook_link, bio, city_arabic) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (profile_id, name, email, gender, city, street, hashed, 0, 0, '', '', '', city_arabic))
    
    print("before commit")
    
    db.commit()
    
    print("done")
    
    user_id = db.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()[0]
    
    db.close()
    
    session['user_id'] = user_id
    
    redirect_url = url_for('front.settings')
    response = make_response()
    response.headers['HX-Redirect'] = redirect_url
    
    return response
    

@user_bp.route('/api/user/login', methods=['POST'], endpoint='user_login')
def user_login():
    db = get_db()
    
    form_email = request.form.get('email').strip()
    form_password = request.form.get('password').strip()

    user = db.execute('SELECT * FROM users WHERE email = ?', (form_email,)).fetchone()
    db.close()
    
    if user and check_password_hash(user['password_hash'], form_password):
        session.clear()
        session['user_id'] = user['id']
        redirect_url = url_for('front.dashboard')
        response = make_response()
        response.headers['HX-Redirect'] = redirect_url
        
        return response


@user_bp.route('/api/user/<int:user_id>/update-settings', methods=['POST'])
def update_settings(user_id):
    db = get_db()
    bio = request.form.get('bio')
    wp_number = request.form.get('whatsapp-number')
    fb_link = request.form.get('facebook-link')
    profile_photo = request.files.get('profile-photo')
    cover_photo = request.files.get('cover-photo')
    
    profile_photo_filename = ""
    cover_photo_filename = ""
    
    if profile_photo and profile_photo.filename:
        profile_photo.save(os.path.join('uploads', profile_photo.filename))
        profile_photo_filename = os.path.join('uploads', profile_photo.filename)
        
    if cover_photo and cover_photo.filename:
        cover_photo.save(os.path.join('uploads', cover_photo.filename))
        cover_photo_filename = os.path.join('uploads', cover_photo.filename)
    
    db.execute('UPDATE users SET bio = ?, whatsapp_number = ?, facebook_link = ?, profile_photo = ?, cover_photo = ? WHERE id = ?', (bio, wp_number, fb_link, profile_photo_filename, cover_photo_filename, user_id,))
    
    db.commit()
    db.close()
    
    redirect_url = url_for('front.profile')
    response = make_response()
    response.headers['HX-Redirect'] = redirect_url
    return response


@user_bp.route('/api/user/<int:user_id>/friends', methods=['GET'])
def get_friends(user_id):
    db = get_db()
    friend_ids = db.execute('SELECT friend_id FROM friends WHERE user_id = ?', (user_id,)).fetchall()
    
    friend_ids = [row['friend_id'] for row in friend_ids]  # list of friend IDs
    
    html_code = ""
    user_icon = url_for('static', filename='icons/user-circle.svg')
    plus_icon = url_for('static', filename='icons/plus.svg')
    
    for friend_id in friend_ids:
        friend_name = db.execute('SELECT name FROM users WHERE id = ?', (friend_id,)).fetchone()
        html_code += f"""<li>
            <div>
                <img src="{user_icon}" alt="user icon" style="width: 2rem;">
                {friend_name}
            </div>
            <button>
                إضافة صديق <img src="{plus_icon}" alt="plus icon">
            </button>
        </li>"""
     
    db.close()
    
    return html_code


@user_bp.route('/api/user/get-all', methods=['GET'])
def get_all():
    try:
        db = get_db()
        users = db.execute('SELECT * FROM users').fetchall()
        db.close()
        users_list = []
        
        for user in users:
            users_list.append(dict(user))
        
        return jsonify({
            'users': users_list,
            'count': len(users_list)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/api/user/<int:user_id>/delete', methods=['POST'], endpoint='user_delete')
def user_delete(user_id):
    db = get_db()
    
    db.execute("DELETE FROM users WHERE id = ?", (user_id,)).fetchone()
    db.commit()
    db.close()
    
    try:
        if session['user_id']:
            session.pop('user_id', None)
    except: 
        print("")
    
    response = make_response()
    
    try:
        if session['admin_id']:
            response = make_response('تم حذف المستخدم بنجاح!')
            response.headers['HX-Trigger'] = 'contentUpdated' 
    except KeyError:
        redirect_url = url_for('front.home')
        response.headers['HX-Redirect'] = redirect_url
        
    return response


@user_bp.route('/api/user/<int:user_id>/searches')
def get_searches(user_id):
    db = get_db()
    
    rows = db.execute("SELECT receiver_id FROM profile_visits WHERE visitor_id = ? ORDER BY visited_at DESC", (user_id,)).fetchall()
    
    receiver_ids = [row[0] for row in rows]
    html_code = ""
    
    
    for receiver_id in receiver_ids:
        receiver = db.execute("SELECT name, city, profile_id FROM users WHERE id = ?", (receiver_id,)).fetchone()
        
        html_code += f"""
          <a href="/profile/{receiver['profile_id']}" style="text-decoration: none;">
            <article style="display: flex; flex-direction: column; justify-content: space-between;">
              <p>{receiver['name']}</p>
              <div style="align-self: flex-end">
                <p class="pico-background-yellow-700" style="border-radius: 13px; padding: 10px;">{receiver['city']}</p>
              </div>
            </article>
          </a>  
        """
        
        
    db.close()
    response = make_response(html_code)
    response.headers['HX-Trigger'] = 'contentUpdated'  # Trigger client event
    return response


@user_bp.route('/api/user/<int:user_id>/last-bill', endpoint="last_bill")
def last_bill(user_id):
    db = get_db()
    
    rows = db.execute("SELECT cost FROM bills WHERE user_id = ? ORDER BY month DESC", (user_id,)).fetchone()
    
    print(f"COST: {rows['cost']}")
    
    try:
        response = make_response(f"{rows['cost']}")
        response.headers['HX-Trigger'] = 'contentUpdated'  # Trigger client event
        return response
    except TypeError:
        response = make_response("0")
        response.headers['HX-Trigger'] = 'contentUpdated'  # Trigger client event
        return response


@user_bp.route('/api/user/<int:user_id>/rank')
def get_user_rank(user_id):
    from datetime import datetime
    db = get_db()
    
    now = datetime.now()
    month = now.month
    rows = db.execute("SELECT user_id FROM bills WHERE month = ? ORDER BY cost DESC", (month,)).fetchall()
    user_ids = [row["user_id"] for row in rows]
    
    indx = user_ids.index(user_id)
    db.close()
    
    response = make_response(f"{indx + 1}")
    response.headers['HX-Trigger'] = 'contentUpdated'  # Trigger client event
    return response
    
    

@user_bp.route('/api/ranking')
def get_ranking():
    from datetime import datetime
    db = get_db()
    
    now = datetime.now()
    month = now.month
    
    rows = db.execute("SELECT * FROM bills WHERE month = ? ORDER BY cost ASC", (month,)).fetchall()
    list_of_rows = [dict(row) for row in rows]
    ordered_bills = list({frozenset(d.items()): d for d in list_of_rows}.values()) # from python docs*
    
    print(f"Ordered bills: {ordered_bills}")
    
    html_code = ""
    html_rows = 0
    
    for x in ordered_bills:
        user = db.execute("SELECT * FROM users WHERE id = ?", (x['user_id'],)).fetchone()
        
        html_code += f"""
            <tr>
                <th scope="row">{html_rows + 1}</th>
                <td><a href="/profile/{user['profile_id']}">{user['name']}</a></td>
                <td>{x['cost']}</td>
            </tr>
        """
        
        html_rows += 1
    
    db.close()
    
    response = make_response(html_code)
    response.headers['HX-Trigger'] = 'contentUpdated'  # Trigger client event
    return response
    
    
@user_bp.route('/api/user/<int:user_id>/increase/xp/<int:value>', methods=['POST'], endpoint="increase_xp")
def increase_xp(user_id, value):
    from datetime import datetime, timedelta
    db = get_db()
    db.execute("UPDATE users SET xp = xp + ? WHERE id = ?", (value, user_id,))
    
    today = datetime.now()
    today = datetime.today()
    today = datetime.now().date()
    
    try:
        if session['last_finished_todo_date']:
            if session['last_finished_todo_date'] == today + timedelta(days=1):
                db.execute("UPDATE users SET streak = streak + 1 WHERE id = ?", (user_id,))
            else:
                db.execute("UPDATE users SET streak = 0 WHERE id = ?", (user_id,))
    except KeyError:
        session['last_finished_todo_date'] = today
        db.execute("UPDATE users SET streak = 1 WHERE id = ?", (user_id,))
    
    db.commit()
    db.close()


@user_bp.route('/api/users')
def get_users():
    db = get_db()
    
    users = db.execute("SELECT * FROM users")
    
    html_code = ""
    
    for x in users:
        html_code += f"""
            <tr class="user-row">
                <th scope="row">{x['name']}</th>
                <td>{x['gender']}</td>
                <td>{x['city_arabic']}</td>
                <td>{x['street']}</td>
                <td>{x['email']}</td>
                <td><a href="/profile/{x['profile_id']}" target="_blank">{x['profile_id']}</a></td>
                <td>{x['streak']}</td>
                <td>{x['xp']}</td>
                <td>{x['joined_at']}</td>
                <td><button class="pico-background-red-600" style="border: 0;" hx-post="/api/user/{x['id']}/delete" hx-target="#output" hx-swap="textContent">حذف</button></td>
            </tr>
        """
    
    db.close()
    
    response = make_response(html_code)
    response.headers['HX-Trigger'] = 'contentUpdated'  # Trigger client event
    return response
