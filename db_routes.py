import os
from flask import *
from app import app
from main import get_db_connection
from models import login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from psycopg2.extras import RealDictCursor
import uuid

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/me')
@login_required
def get_me():
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT idusers as id, bio, avatar_url, username FROM users WHERE idusers = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close(); conn.close()
    return jsonify(user)

@app.route('/api/add-activity', methods=['POST'])
@login_required
def add_activity():
    data = request.get_json()
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
    "INSERT INTO activities (name, class, due_date, description, status, user_id) VALUES (%s, %s, %s, %s, 'pending', %s)",
    (data['name'], data['class'], data['due_date'], data['description'], user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Task added'}), 201

@app.route('/api/activities')
@login_required
def get_activities():
    user_id = session['user_id']
    status = request.args.get('status', 'pending')
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor) 
    cursor.execute("SELECT * FROM activities WHERE status = %s AND user_id = %s ORDER BY due_date",(status, user_id,))
    activities = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(activities)

@app.route('/api/finish-activity/<int:task_id>', methods=['PUT'])
@login_required
def finish_activity(task_id):
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("UPDATE activities SET status = 'completed' WHERE id = %s AND user_id = %s", (task_id, user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Task finished'}), 200

@app.route('/api/delete-activity/<int:task_id>', methods=['DELETE'])
@login_required
def delete_activity(task_id):
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("DELETE FROM activities WHERE id = %s AND user_id = %s", (task_id, user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Task deleted'}), 200

@app.route('/api/activities/<int:task_id>', methods=['PUT'])
@login_required
def update_activity(task_id):
    user_id = session['user_id']
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid data'}), 400
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("UPDATE activities SET name = %s, class = %s, due_date = %s, description = %s WHERE id = %s AND user_id = %s", 
    (data['name'], data['class'], data['due_date'], data['description'], task_id, user_id))
    conn.commit()
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify({'error': 'Task not found'}), 404
    cursor.close()
    conn.close()
    return jsonify({'message': 'Task updated'}), 200

# Your existing schedule route (unchanged)
@app.route('/api/schedule')
def get_schedule():
    # Your code to fetch schedule from DB or static data
    return jsonify(your_schedule_data) # type: ignore

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nome = request.form['nomeForm']
        senha = request.form['passwordForm']
        senha_hash = generate_password_hash(senha)
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM users WHERE nome = %s", (nome,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            flash('Usuário já está em uso')
            return render_template('register.html')
        cursor.execute(
            "INSERT INTO users (nome, username, password) VALUES (%s, %s, %s) RETURNING idusers",
            (nome, nome, senha_hash)
        )
        user = cursor.fetchone()
        user_id = user['idusers']
        conn.commit()
        session['user_id'] = user_id
        cursor.close()
        conn.close()
        return redirect(url_for('homepage'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nomeForm']
        senha = request.form['passwordForm']
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            "SELECT * FROM users WHERE nome = %s",
            (nome,)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user and check_password_hash(user['password'], senha):
            session['user_id'] = user['idusers']
            return redirect(url_for('homepage'))
        else:
            flash('Login Inválido')
    return render_template('login.html')

@app.route('/api/profile/<int:user_id>')
@login_required
def get_profile(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM users WHERE idusers = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(dict(user))

@app.route('/api/update-profile', methods=['POST'])
@login_required
def update_profile():
    user_id = session['user_id']
    username = request.form.get('nome')
    bio = request.form.get('bio')
    file = request.files.get('avatar')
    avatar_url = None
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        upload_folder = app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        ext = filename.split('.')[-1]
        unique_name = f"{uuid.uuid4()}.{ext}"
        filepath = os.path.join(upload_folder, unique_name)
        file.save(filepath)
        avatar_url = f'/static/uploads/{unique_name}'
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    if avatar_url:
        cursor.execute("UPDATE users SET username = %s, bio = %s, avatar_url = %s WHERE idusers = %s", (username, bio, avatar_url, user_id))
    else:
        cursor.execute("UPDATE users SET username = %s, bio = %s WHERE idusers = %s", (username, bio, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Perfil atualizado'})