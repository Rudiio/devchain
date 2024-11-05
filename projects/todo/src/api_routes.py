from flask import Blueprint, request, jsonify
from task_manager import TaskManager

api_blueprint = Blueprint('api', __name__)
task_manager = TaskManager()

@api_blueprint.route('/add_task', methods=['POST'])
def add_task():
    data = request.get_json()
    description = data.get('description', '')
    if description:
        task_manager.add_task(description)
        return jsonify({'message': 'Task added successfully'}), 201
    else:
        return jsonify({'message': 'Description is required'}), 400

@api_blueprint.route('/change_task_status/<int:task_id>', methods=['PUT'])
def change_task_status(task_id):
    task = next((task for task in task_manager.get_tasks() if task['id'] == task_id), None)
    if task:
        task_manager.change_task_status(task_id)
        return jsonify({'message': 'Task status updated successfully'}), 200
    else:
        return jsonify({'message': 'Task not found'}), 404

@api_blueprint.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = next((task for task in task_manager.get_tasks() if task['id'] == task_id), None)
    if task:
        task_manager.delete_task(task_id)
        return jsonify({'message': 'Task deleted successfully'}), 200
    else:
        return jsonify({'message': 'Task not found'}), 404

@api_blueprint.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = task_manager.get_tasks()
    return jsonify(tasks), 200
