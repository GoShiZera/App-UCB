from flask import *
from app import app
from main import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/api/add-activity', methods=['POST'])
def add_activity():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO activities (name, class, due_date, description) VALUES (%s, %s, %s, %s)",
        (data['name'], data['class'], data['due_date'], data['description'])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Task added'}), 201

@app.route('/api/activities')
def get_activities():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # For MySQL; use row_factory for SQLite
    cursor.execute("SELECT * FROM activities WHERE status = 'pending' ORDER BY due_date")
    activities = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(activities)

@app.route('/api/finish-activity/<int:task_id>', methods=['PUT'])
def finish_activity(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE activities SET status = 'completed' WHERE id = %s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Task finished'}), 200

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
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE nome = %s", (nome,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            flash('Usuário já está em uso')
            return render_template('register.html')
        cursor.execute(
            "INSERT INTO users (nome, password) VALUES (%s, %s)",
            (nome, senha_hash)
        )
        conn.commit()
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
        cursor = conn.cursor(dictionary=True)
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