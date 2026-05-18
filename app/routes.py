from flask import Blueprint, jsonify, request, render_template, current_app
from app.models import Task

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@bp.route('/info', methods=['GET'])
def info():
    return jsonify({
        "app": "Task Manager API",
        "version": current_app.config["APP_VERSION"],
        "max_tasks": current_app.config["MAX_TASKS"]
    }), 200

@bp.route('/tasks', methods=['GET', 'POST'])
def handle_tasks():
    tasks = current_app.config['TASKS']
    
    if request.method == 'GET':
        return jsonify([task.to_dict() for task in tasks]), 200

    if request.method == 'POST':
        data = request.get_json() or {}
        if 'title' not in data or not str(data['title']).strip():
            return jsonify({"error": "'title' is required"}), 400
        
        if len(tasks) >= current_app.config['MAX_TASKS']:
            return jsonify({"error": "Task limit (N) reached"}), 409

        current_app.config['TASK_COUNTER'] += 1
        new_id = current_app.config['TASK_COUNTER']
        
        new_task = Task(
            task_id=new_id,
            title=data['title'],
            description=data.get('description', '')
        )
        tasks.append(new_task)
        return jsonify(new_task.to_dict()), 201

@bp.route('/tasks/<int:task_id>', methods=['GET', 'PATCH', 'DELETE'])
def handle_single_task(task_id):
    tasks = current_app.config['TASKS']
    task = next((t for t in tasks if t.id == task_id), None)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    if request.method == 'GET':
        return jsonify(task.to_dict()), 200

    if request.method == 'PATCH':
        data = request.get_json() or {}
        if 'done' not in data:
            return jsonify({"error": "'done' field is required"}), 400
        
        task.done = bool(data['done'])
        return jsonify(task.to_dict()), 200

    if request.method == 'DELETE':
        tasks.remove(task)
        return jsonify({"message": "Task deleted", "task": task.to_dict()}), 200
