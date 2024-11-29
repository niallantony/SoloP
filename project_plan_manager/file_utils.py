import json
from json import JSONDecodeError

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

