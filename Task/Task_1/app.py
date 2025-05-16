
from flask import Flask, jsonify, request
import datetime
import threading

from notifications import TaskNotification

app = Flask(__name__)
tasks = [
    {'id': 1, 'title': 'Grocery Shopping', 'completed': False, 'due_date': '2024-03-15'},
    {'id': 2, 'title': 'Pay Bills', 'completed': False, 'due_date': '2024-03-20'},
]
next_task_id = 3  # For assigning new task IDs


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)


@app.route('/api/tasks', methods=['POST'])
def create_task():
    global next_task_id
    data = request.get_json()
    new_task = {
        'id': next_task_id,
        'title': data['title'],
        'completed': False,
        'due_date': data.get('due_date') or datetime.date.today().strftime("%Y-%m-%d")
    }
    next_task_id += 1
    tasks.append(new_task)
    return jsonify(new_task), 201


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task['id'] == task_id:
            task.update(data)  # Update task attributes

            """
                This launches a background thread to send a notification for task update
                This ensures the notification process runs asynchronously, without blocking the main thread.
            """
            threading.Thread(
                target=TaskNotification.send_update_notification,
                args=(task_id,)
            ).start()

            return jsonify(task), 200
    return jsonify({'error': 'Task not found'}), 404


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            del tasks[i]
            return jsonify({'message': 'Task deleted'}), 204
    return jsonify({'error': 'Task not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)

"""
    EXPLANATION:
    
    Existing problem: 
        The original update_task route included a blocking time.sleep(2) to simulate sending a notification, 
        which delayed API response by blocking the main thread during execution.
    
    Updated solution:
        Moved the notification logic to a separate class method
        TaskNotification.send_update_notification() to improve code organization and maintainability.
        
        Used threading to run the notification method asynchronously
        in the background when a task is updated.
        
        The threading approach allows the API to respond immediately without waiting for the notification process
        to complete, thereby improving the performance of the API
        
        The reason why I've used threading is,
            Blocking of main thread can lead to performance bottlenecks.
            Threading offering concurrency on managing multiple tasks.
            It runs in the background without blocking the main request-response cycle
        
"""
