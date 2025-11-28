import sqlite3
import bcrypt

def signup(name, email, password):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    if cur.fetchone():
        return False

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    cur.execute("INSERT INTO users(name, email, password) VALUES(?,?,?)", (name, email, hashed_pw))
    conn.commit()
    return True


def login(email, password):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cur.fetchone()

    if user and bcrypt.checkpw(password.encode(), user[3]):
        return user
    return None
