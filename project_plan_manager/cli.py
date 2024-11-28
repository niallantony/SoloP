import argparse
from plan_manager import add_task, delete_task, change_file, change_status

def main():
    parser = argparse.ArgumentParser(description="Task Manager")
    parser.add_argument('--add', type=str, help="Add a new task")
    parser.add_argument('--delete', type=int, help="Delete a task by ID")
    parser.add_argument('--status', nargs=2, help="Change a status message, takes an ID and new status")

    args = parser.parse_args()

    if args.add:
        change_file(add_task, args.add)
    elif args.delete:
        change_file(delete_task, args.delete)
    elif args.status:
        change_file(change_status, int(args.status[0]), args.status[1])
        
if __name__ == "__main__":
    main()