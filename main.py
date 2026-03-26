from flask import Flask, request, jsonify
import psycopg2
import os

from app import app

def get_db_connection():
    database_url = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(
        database_url,
        sslmode="require")
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        idusers SERIAL PRIMARY KEY,
        nome TEXT UNIQUE,
        username TEXT,
        password TEXT,
        bio TEXT,
        avatar_url TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activities (
        id SERIAL PRIMARY KEY,
        name TEXT,
        class TEXT,
        due_date TEXT,
        description TEXT,
        status TEXT,
        user_id INTEGER REFERENCES users(idusers)
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()
init_db()

from routes import *
from db_routes import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)