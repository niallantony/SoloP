import argparse
from project_plan_manager.task_utils import add_task, delete_task, change_status
from project_plan_manager.file_utils import (
    change_tasks,
    load_tasks,
    load_file,
    change_meta,
)
from project_plan_manager.md_writer import (
    MDWriter
)

def main():
    parser = argparse.ArgumentParser(description="Task Manager")
    parser.add_argument('--add', type=str, help="Add a new task")
    parser.add_argument('--delete', type=int, help="Delete a task by ID")
    parser.add_argument('--status', nargs=2, help="Change a status message, takes an ID and new status")
    parser.add_argument('--xmake', action="store_false", help="Include to make adjustments without writing to SOLOP file")
    parser.add_argument('--rename', type=str, help="Rename the project with a given string")

    args = parser.parse_args()
    print(vars(args))
    executer = CommandExecuter(args)
    executer.execute_commands()

class CommandExecuter:
    def __init__(self, args):
        self.args = args
        self.actions = {
            'xmake':self.make, "'xmake' by default is true, calling xmake won't run make"
            'rename':self.rename,
            'add':self.add,
            'delete':self.delete,
            'status':self.status,
        }

    def execute_commands(self):
        passed = vars(self.args)
        flags = passed.keys()
        for flag in flags:
            if not passed[flag]:
                print(f"Didn't execute {flag}")
                continue
            self.actions[flag](passed[flag])

    def make(self, _):
        file = load_file()
        writer = MDWriter(file['project'], file['tasks'])
        writer.write_md_file()

    def rename(self,name):
        change_meta('project', name)

    def add(self,description):
        change_tasks(add_task, description)
        
    def delete(self,task_id):
        try:
            change_tasks(delete_task,task_id)
        except (StopIteration):
            print("Task not found")

    def status(self, args):
        status_message = args.pop(0)
        if len(args) == 0:
            print("--status expects 1+ arguments for IDs")
        try:
            args = self.as_ints(args)
            for id in args:
                
                id = int(id)
                print(id)
                change_tasks(change_status,id, status_message)
        except (StopIteration):
            print("Task not found")
        except (ValueError):
            print("Please supply IDs as Integers")
    
    def as_ints(self, list):
        newlist = []
        for element in list:
            try:
                element = int(element)
                newlist.append(element)
            except (ValueError):
                raise ValueError
        return newlist


if __name__ == "__main__":
    main()