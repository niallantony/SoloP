import re

class Task:
    def __init__(self, id, description, status="backlog", parent=None) -> None:
        self.id = id
        self.description = description
        self.status = status
        self.children = []
        self.parent = parent
    
    def as_string(self):
        return f"- [{self.id}]: {self.description}"
        
class InvalidTaskError(Exception):
    """
    Exception raised for invalid task inputs (ie. Empty descriptions)
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def as_task_object(task):
    """
    Converts the dictionaries from JSON to Task objects
    """
    return Task(id = task['id'],
                description= task['description'],
                status=task.setdefault("status","backlog")
                )

def get_task(tasks, task_id):
    task = next(task for task in tasks if task['id'] == task_id)
    return as_task_object(task)

def get_of_status(tasks, status):
    of_status = []
    for task in tasks:
        if "status" not in task.keys():
            continue
        if task['status'] == status:
            of_status.append(as_task_object(task))
    return of_status

def add_task(tasks, description):
    assert isinstance(description, str), f"Expected a string, got {type(description).__name__}"
    if (len(description) == 0):
        raise InvalidTaskError("Invalid Task Description")
    newlines = re.findall("^", description, flags=re.M)
    if len(newlines) > 1:
        raise InvalidTaskError("Multi-line tasks not supported")
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