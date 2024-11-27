import json

class Task:
    def __init__(self, id, description, status="backlog") -> None:
        self.id = id
        self.description = description
        self.status = status
        
def load_tasks():
    try:
        with open('tasks.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f, indent=4)

def add_task(description):
    tasks = load_tasks()
    new_task = Task(id=len(tasks)+1, description=description)
    tasks.append(new_task.__dict__)
    save_tasks(tasks)

def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)