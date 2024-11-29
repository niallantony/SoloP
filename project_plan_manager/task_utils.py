from project_plan_manager.file_utils import load_tasks

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

def get_task(task_id):
    tasks = load_tasks()
    task = next(task for task in tasks if task['id'] == task_id)
    return task    

def get_of_status(status):
    tasks = load_tasks()
    of_status = []
    for task in tasks:
        if task['status'] == status:
            of_status.append(task)
    return of_status

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