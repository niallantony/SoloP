import argparse
from plan_manager import add_task, delete_task

def main():
    parser = argparse.ArgumentParser(description="Task Manager")
    parser.add_argument('--add', type=str, help="Add a new task")
    parser.add_argument('--delete', type=int, help="Delete a task by ID")

    args = parser.parse_args()

    if args.add:
        add_task(args.add)
    elif args.delete:
        delete_task(args.delete)
        
if __name__ == "__main__":
    main()