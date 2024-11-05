# /task_manager.py
from json_storage import JsonStorage

class TaskManager:
    def __init__(self):
        self.storage = JsonStorage('tasks.json')
        self.tasks = self.storage.read_tasks()
        self.next_id = max(task['id'] for task in self.tasks) + 1 if self.tasks else 1

    def add_task(self, description):
        task = {
            'id': self.next_id,
            'description': description,
            'status': 'open'
        }
        self.tasks.append(task)
        self.storage.write_tasks(self.tasks)
        self.next_id += 1

    def change_task_status(self, task_id):
        for task in self.tasks:
            if task['id'] == task_id:
                task['status'] = 'closed'
                self.storage.write_tasks(self.tasks)
                break

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task['id'] != task_id]
        self.storage.write_tasks(self.tasks)

    def get_tasks(self):
        return self.tasks
