import sqlite3
import os
from random import randint
from flask import session
from werkzeug.security import generate_password_hash


DB_PATH = 'database.db'


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def new_profile_id():
    db = get_db()
    rand_id = randint(11111111, 99999999)
    
    db_profile_ids = db.execute('SELECT profile_id FROM users').fetchall() 
    profile_ids = [row[0] for row in db_profile_ids]
    
    while True:
        if rand_id in profile_ids:
            rand_id = randint(11111111, 99999999)
        else:
            break
    
    db.close()
    return rand_id


def init_db():
    conn = get_db()
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER UNIQUE,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            gender TEXT NOT NULL,
            city TEXT NOT NULL,
            city_arabic TEXT NOT NULL, 
            street TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            xp INTEGER, 
            streak INTEGER,
            facebook_link TEXT,
            whatsapp_number TEXT,
            bio TEXT
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS collectors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code INTEGER NOT NULL,
            password_hash TEXT NOT NULL,
            city TEXT NOT NULL,
            street TEXT NOT NULL,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS bills (
            user_id INTEGER NOT NULL,
            collector_id INTEGER NOT NULL,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            cost INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(collector_id) REFERENCES collectors(id)
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS profile_visits (
            visitor_id INTEGER,
            receiver_id INTEGER,
            visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(visitor_id) REFERENCES users(id),
            FOREIGN KEY(receiver_id) REFERENCES users(id),
            PRIMARY KEY (visitor_id, receiver_id)
        );
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()


def make_fakes():
    conn = get_db()
    
    # Adding fake admin
    pass_hash1 = generate_password_hash('this123omar')
    
    conn.execute("INSERT INTO admins (username, password_hash) VALUES ('omar123', ?)", (pass_hash1,))
    
    # Adding fake collector
    pass_hash2 = generate_password_hash('this_is_my_password_95')
    
    conn.execute("INSERT INTO collectors (name, code, password_hash, city, street) VALUES ('هاني مسعد','123456', ?, 'الإسكندرية', 'محرم بك')", (pass_hash1,))
    
    # Adding fake user
    pass_hash3 = generate_password_hash('fake_pass')
    fake_profile = new_profile_id()
    fake_bio = "السلام عليكم 👋 انا عمر حسام مبرمج و مطور مواقع عمري 16 سنة من الإسكندرية!"
    
    conn.execute("INSERT INTO users (name, email, gender, city, street, city_arabic, xp, streak, password_hash, profile_id, bio, whatsapp_number, facebook_link) VALUES ('عمر حسام','omar@example.com', 'male', 'alexandria', 'محرم بك','الإسكندرية',125,4,?,?,?,'01146641222','https://www.facebook.com/omarhossam160')", (pass_hash3, fake_profile, fake_bio))
    
    conn.commit()
    conn.close()
