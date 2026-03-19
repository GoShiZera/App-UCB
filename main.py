from flask import Flask, request, jsonify
import mysql.connector

from app import app

def get_db_connection():
    return mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'Lorem Ipsum',
        database = 'ucb_project'
    )
from routes import *
from db_routes import *

if __name__ == '__main__':
    app.run(host='your ip', debug=True)