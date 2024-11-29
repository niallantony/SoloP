import json
from json import JSONDecodeError

class Task:
    def __init__(self, id, description, status="backlog") -> None:
        self.id = id
        self.description = description
        self.status = status
        
class InvalidTaskError(Exception):
    """
    Exception raised for invalid task inputs (ie. Empty descriptions)
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def load_tasks():
    try:
        with open('tasks.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except JSONDecodeError:
        return []


def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f, indent=4)

def change_file(action, *args, **kwargs):
    tasks = load_tasks() or []
    modified = action(tasks, *args, **kwargs)
    save_tasks(modified)
    return modified

def add_task(tasks, description):
    assert isinstance(description, str), f"Expected a string, got {type(description).__name__}"
    if (len(description) == 0):
        raise InvalidTaskError("Invalid Task Description")
    new_task = Task(id=len(tasks)+1, description=description)
    new_tasks = tasks.copy()
    new_tasks.append(new_task.__dict__)
    return new_tasks

def delete_task(tasks, task_id):
    delete_task = next(task for task in tasks if task["id"] == task_id)
    new_tasks = [task for task in tasks if task != delete_task]
    return new_tasks

def change_status(tasks, task_id, status):
    task = next(task for task in tasks if task['id'] == task_id)
    tasks[tasks.index(task)]['status'] = status
    return tasks