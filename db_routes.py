from flask import *
from app import app
from main import get_db_connection

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