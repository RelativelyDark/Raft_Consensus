from flask import Flask, request, jsonify, render_template
import mysql.connector

# Define constants for task statuses
TODO = 'TODO'
IN_PROGRESS = 'IN_PROGRESS'
COMPLETED = 'COMPLETED'

# Initialize Flask app
app = Flask(_name_)

# Configure MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="R4rathima",
    database="tasks"
)

# Define a class to represent a Task
class Task:
    def _init_(self, id, title, description, status=TODO):
        self.id = id
        self.title = title
        self.description = description
        self.status = status

# Define the root route to render the index.html template
@app.route('/')
def index():
    return render_template('index.html')

# Define API endpoints for task management
@app.route("/tasks", methods=['GET'])
def get_tasks():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    serialized_tasks = [{"id": task[0], "title": task[1], "description": task[2], "status": task[3]} for task in tasks]
    return jsonify(serialized_tasks)

@app.route("/tasks", methods=['POST'])
def create_task():
    data = request.json
    title = data['title']
    description = data['description']
    status = data.get('status', TODO)
    cursor = db.cursor()
    cursor.execute("INSERT INTO tasks (title, description, status) VALUES (%s, %s, %s)", (title, description, status))
    db.commit()
    cursor.close()
    return "Task created successfully", 201

@app.route("/tasks/<int:task_id>", methods=['GET'])
def get_task(task_id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cursor.fetchone()
    cursor.close()
    if task:
        return jsonify({"id": task[0], "title": task[1], "description": task[2], "status": task[3]})
    else:
        return "Task not found", 404

@app.route("/tasks/<int:task_id>", methods=['PUT'])
def update_task(task_id):
    data = request.json
    title = data.get('title')
    description = data.get('description')
    status = data.get('status')
    cursor = db.cursor()
    cursor.execute("UPDATE tasks SET title = %s, description = %s, status = %s WHERE id = %s", (title, description, status, task_id))
    db.commit()
    cursor.close()
    return "Task updated successfully"

@app.route("/tasks/<int:task_id>", methods=['DELETE'])
def delete_task(task_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    db.commit()
    cursor.close()
    return "Task deleted successfully", 200

# Run the Flask app
if _name_ == "_main_":
    app.run(debug=True)