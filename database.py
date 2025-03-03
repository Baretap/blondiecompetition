import sqlite3

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        profile_pic TEXT,
        referral_code TEXT NOT NULL UNIQUE,
        referrer_id INTEGER,
        points REAL DEFAULT 50,
        FOREIGN KEY (referrer_id) REFERENCES users(id)
    )''')
    conn.commit()
    conn.close()

def add_user(username, email, password, profile_pic, referral_code):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, email, password, profile_pic, referral_code, points) VALUES (?, ?, ?, ?, ?, ?)',
              (username, email, password, profile_pic, referral_code, 50))
    user_id = c.lastrowid
    conn.commit()
    conn.close()
    return user_id

def get_user_by_username(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT username, email, profile_pic, points, referral_code FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user

def get_leaderboard():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT username, points FROM users ORDER BY points DESC LIMIT 10')
    users = c.fetchall()
    conn.close()
    return users

def get_user_by_referral_code(referral_code):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT id, points FROM users WHERE referral_code = ?', (referral_code,))
    user = c.fetchone()
    conn.close()
    return user

def update_points(user_id, points):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('UPDATE users SET points = points + ? WHERE id = ?', (points, user_id))
    conn.commit()
    conn.close()
