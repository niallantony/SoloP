import argparse
from task_utils import add_task, delete_task, change_status
from file import change_file

def main():
    parser = argparse.ArgumentParser(description="Task Manager")
    parser.add_argument('--add', type=str, help="Add a new task")
    parser.add_argument('--delete', type=int, help="Delete a task by ID")
    parser.add_argument('--status', nargs=2, help="Change a status message, takes an ID and new status")

    args = parser.parse_args()

    if args.add:
        add(args.add)
    elif args.delete:
        delete(args.delete)
    elif args.status:
        status(int(args.status[0]), args.status[1])
        
def add(description):
    change_file(add_task, description)
    
def delete(task_id):
    try:
        change_file(delete_task,task_id)
    except (StopIteration):
        print("Task not found")

def status(task_id, status):
    try:
        change_file(change_status,task_id, status)
    except (StopIteration):
        print("Task not found")


if __name__ == "__main__":
    main()