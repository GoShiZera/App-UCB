from flask import Flask, request, jsonify
import sqlite3

from app import app

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        idusers INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE,
        password TEXT
        bio TEXT DEFAULT '',
        avatar_url TEXT DEFAULT ''
    )
    """)

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN bio TEXT DEFAULT ''")
    except:
        pass

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN avatar_url TEXT DEFAULT ''")
    except:
        pass

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        class TEXT,
        due_date TEXT,
        description TEXT,
        status TEXT,
        user_id INTEGER
    )
    """)

    conn.commit()
    conn.close()
init_db()

from routes import *
from db_routes import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)