from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "tasks.json"

# Load tasks
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

def read_tasks():
    with open(DATA_FILE) as f:
        return json.load(f)

def write_tasks(tasks):
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

@app.route("/")
def hello():
    return jsonify({"message": "Welcome to the ToDo List API"})

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(read_tasks())

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    tasks = read_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "task": data.get("task"),
        "done": False
    }
    tasks.append(new_task)
    write_tasks(tasks)
    return jsonify(new_task), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def mark_done(task_id):
    tasks = read_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            write_tasks(tasks)
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = read_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    write_tasks(tasks)
    return jsonify({"message": f"Task {task_id} deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
