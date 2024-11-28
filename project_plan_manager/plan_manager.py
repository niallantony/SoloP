import json

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

def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f, indent=4)

def add_task(description):
    assert isinstance(description, str), f"Expected a string, got {type(description).__name__}"
    tasks = load_tasks()
    if (len(description) == 0):
        raise InvalidTaskError("Invalid Task Description")
    new_task = Task(id=len(tasks)+1, description=description)
    tasks.append(new_task.__dict__)
    save_tasks(tasks)

def delete_task(task_id):
    tasks = load_tasks()
    delete_task = next(task for task in tasks if task["id"] == task_id)
    new_tasks = [task for task in tasks if task != delete_task]
    save_tasks(new_tasks)