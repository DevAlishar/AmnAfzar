from flask import Blueprint, request, jsonify
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/", methods=["GET"])
def get_tasks():
    """
    Get all tasks
    ---
    responses:
      200:
        description: A list of tasks
    """
    tasks = Task.query.all()
    return jsonify([{"id": task.id, "title": task.title, "description": task.description} for task in tasks]), 200

@tasks_bp.route("/<int:task_id>", methods=["GET"])
def get_task(task_id):
    """
    Get a task by ID
    ---
    parameters:
      - name: task_id
        type: integer
        required: true
        description: ID of the task
    responses:
      200:
        description: Task details
      404:
        description: Task not found
    """
    task = Task.query.get(task_id)
    if task:
        return jsonify({"id": task.id, "title": task.title, "description": task.description}), 200
    return jsonify({"error": "Task not found"}), 404

@tasks_bp.route("/", methods=["POST"])
def create_task():
    """
    Create a new task
    ---
    parameters:
      - name: title
        type: string
        required: true
        description: Title of the task
      - name: description
        type: string
        required: false
        description: Description of the task
    responses:
      201:
        description: Task created successfully
      400:
        description: Missing fields
    """
    data = request.json
    title = data.get("title")
    description = data.get("description", "")

    if not title:
        return jsonify({"error": "Title is required."}), 400

    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"message": "Task created successfully."}), 201

@tasks_bp.route("/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """
    Update a task by ID
    ---
    parameters:
      - name: task_id
        type: integer
        required: true
        description: ID of the task
      - name: title
        type: string
        required: false
        description: New title of the task
      - name: description
        type: string
        required: false
        description: New description of the task
    responses:
      200:
        description: Task updated successfully
      404:
        description: Task not found
    """
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.json
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)

    db.session.commit()
    return jsonify({"message": "Task updated successfully."}), 200

@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """
    Delete a task by ID
    ---
    parameters:
      - name: task_id
        type: integer
        required: true
        description: ID of the task
    responses:
      204:
        description: Task deleted successfully
      404:
        description: Task not found
    """
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully."}), 204