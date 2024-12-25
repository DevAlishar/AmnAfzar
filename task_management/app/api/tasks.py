from flask import Blueprint, request, jsonify
from app import db
from app.models.task import Task
from flask import render_template
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__)
@tasks_bp.route("/create", methods=["GET"])
def create_task_page():
    return render_template("create_task.html")
@tasks_bp.route("/", methods=["POST"])
def create_task():
    data = request.json

    new_task = Task(
        user_id=data.get("user_id"),
        title=data.get("title"),
        description=data.get("description"),
        due_date=datetime.strptime(data.get("due_date"), "%Y-%m-%d") if data.get("due_date") else None,
        status=data.get("status", "pending"),
        priority=data.get("priority", "medium")
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"message": "Task created successfully."}), 201