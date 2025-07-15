import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        words_used INTEGER DEFAULT 0,
        last_reset DATE DEFAULT CURRENT_DATE
    )''')
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row

def update_words(user_id, word_count):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    c.execute("UPDATE users SET words_used = words_used + ? WHERE user_id = ?", (word_count, user_id))
    conn.commit()
    conn.close()

def can_convert(user_id, word_count, is_admin=False):
    if is_admin:
        return True
    user = get_user(user_id)
    used = user[1] if user else 0
    return used + word_count <= 1000
