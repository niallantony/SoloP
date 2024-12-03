import argparse
from project_plan_manager.task_utils import (
    add_task,
    delete_task, 
    change_status, 
    change_priority, 
    set_as_child, 
    unset_as_child
)
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
    parser.add_argument('--delete', nargs='+', help="Delete a task by ID")
    parser.add_argument('--status', nargs='*', help="Change a status message, takes an ID and new status")
    parser.add_argument('--rename', type=str, help="Rename the project with a given string")
    parser.add_argument('--priority', nargs='*', help="Changes the priority of tasks to the first given argument")
    parser.add_argument('--child', nargs=2, help="Sets the first arg as the child of the second arg")
    parser.add_argument('--xchild', nargs=1, type=int, help="Un-nest a task from any parents")
    parser.add_argument('--inherit', action="store_true", help="Inherit mode attaches nested tasks to the parent task when unattaching a child")
    parser.add_argument('--xmake', action="store_false", help="Include to make adjustments without writing to SOLOP file")
    parser.add_argument('--all', action="store_true", help="Include to render all tasks to document regardless of given headers")

    args = parser.parse_args()
    executer = CommandExecuter(args)
    executer.execute_commands()

class CommandExecuter:
    def __init__(self, args):
        self.args = args
        self.actions = {
            'xmake':self.make, #'xmake' by default is true, calling xmake won't run make
            'rename':self.rename,
            'add':self.add,
            'delete':self.delete,
            'status':self.status,
            'child':self.child,
            'xchild':self.xchild,
            'priority':self.priority,
            'inherit':self.inherit,
            'all':self.all,
        }

    def execute_commands(self):
        passed = vars(self.args)
        flags = passed.keys()
        for flag in flags:
            if not passed[flag]:
                continue
            self.actions[flag](passed[flag])

    def make(self, _):
        file = load_file()
        writer = MDWriter(file['project'], file['tasks'], file['headers'])
        writer.write_md_file(render_all=self.args.all)
    
    def inherit(self, _):
        pass

    def all(self, _):
        pass

    def rename(self,name):
        change_meta('project', name)

    def add(self,description):
        change_tasks(add_task, description)
        
    def delete(self,args):
        try:
            args = self.as_ints(args) 
            for task_id in args:
                confirm = self.__get_confirmation(f"delete Task [{task_id}]")
                if confirm:
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
    
    def priority(self, args):
        try:
            args = self.as_ints(args)
            priority = args.pop(0)
            for id in args:
                change_tasks(change_priority, id, priority)
        except (ValueError):
            print("Provide a list of IDs as ints only")
    
    def child(self, args):
        try:
            child_id = int(args[0])
            parent_id = int(args[1])
            change_tasks(set_as_child, child_id, parent_id)
        except (StopIteration):
            print("Tasks not found")
        except (ValueError):
            print("Please input IDs as ints only")
    
    def xchild(self, args):
        try:
            change_tasks(unset_as_child, args[0], self.args.inherit)
        except (StopIteration):
            print("Task not found")
        except (ValueError):
            print("Not a nested task")
    
    def __get_confirmation(self, action_string):
        res = input(f"Confirm action [{action_string}](Y/n): ")
        if res.upper() == "Y" or res.upper() == "YES":
            return True
        else:
            return False


if __name__ == "__main__":
    main()