// scripts.js

document.addEventListener('DOMContentLoaded', function() {
    loadTasks();
    document.getElementById('task-form').addEventListener('submit', addTask);
});

function loadTasks() {
    fetch('/api/tasks')
        .then(response => response.json())
        .then(tasks => {
            const taskList = document.getElementById('task-list');
            taskList.innerHTML = '';
            tasks.forEach(task => {
                const taskItem = document.createElement('div');
                taskItem.className = 'task-item';
                taskItem.innerHTML = `
                    <span>${task.description}</span>
                    <div class="status-indicator ${task.status === 'open' ? 'pending' : 'completed'}"></div>
                    <button class="change-status" data-id="${task.id}">${task.status === 'open' ? 'Complete' : 'Reopen'}</button>
                    <button class="delete-task" data-id="${task.id}">Delete</button>
                `;
                taskList.appendChild(taskItem);
            });
            attachStatusChangeListeners();
            attachDeleteListeners();
        })
        .catch(error => console.error('Error loading tasks:', error));
}

function addTask(event) {
    event.preventDefault();
    const taskInput = document.getElementById('task-input');
    const description = taskInput.value.trim();
    if (description) {
        fetch('/api/add_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ description: description }),
        })
        .then(response => response.json())
        .then(() => {
            loadTasks();
            taskInput.value = '';
        })
        .catch(error => console.error('Error adding task:', error));
    }
}

function changeTaskStatus(taskId, newStatus) {
    fetch(`/api/change_task_status/${taskId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus }),
    })
    .then(response => response.json())
    .then(() => loadTasks())
    .catch(error => console.error('Error changing task status:', error));
}

function deleteTask(taskId) {
    fetch(`/api/delete_task/${taskId}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(() => loadTasks())
    .catch(error => console.error('Error deleting task:', error));
}

function attachStatusChangeListeners() {
    document.querySelectorAll('.change-status').forEach(button => {
        button.addEventListener('click', function() {
            const taskId = this.getAttribute('data-id');
            const newStatus = this.textContent === 'Complete' ? 'closed' : 'open';
            changeTaskStatus(taskId, newStatus);
        });
    });
}

function attachDeleteListeners() {
    document.querySelectorAll('.delete-task').forEach(button => {
        button.addEventListener('click', function() {
            const taskId = this.getAttribute('data-id');
            deleteTask(taskId);
        });
    });
}
