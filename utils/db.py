import sqlite3
import os
from random import randint
from flask import session


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
            email TEXT NOT NULL UNIQUE,
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
            gender TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            city TEXT NOT NULL,
            street TEXT NOT NULL,
            province TEXT NOT NULL,
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
        CREATE TABLE IF NOT EXISTS friends (
            user_id INTEGER,
            friend_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(friend_id) REFERENCES users(id),
            PRIMARY KEY (user_id, friend_id)
        );
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS friend_requests (
            receiver_id INTEGER,
            sender_id INTEGER,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(receiver_id) REFERENCES users(id),
            FOREIGN KEY(sender_id) REFERENCES users(id),
            PRIMARY KEY (receiver_id, sender_id)
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
