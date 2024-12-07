import re
from solop.file_utils import load_file

class ListParser:
    def __init__(self):
        self.typenames = {
            '#':ProjectHeader,
            '##':SectionHeader,
            '-':ListItem
        }
        self.listitems = dict({})

    def read_file(self, f):
        try:
            with open(f, 'r') as f:
                return f.readlines()
        except FileNotFoundError:
            print("File not found")
    
    def get_items(self, lines):
        split_lines = [] 
        lines = map(lambda x: x.split(" ", 2), lines)
        lines = filter(lambda x: len(x) > 1, lines)
        lines = filter(lambda x: x[0] != '(', lines)
        return list(lines)
    
    def parse_doc(self, f):
        lines = self.read_file(f)
        lines = self.get_items(lines)
        self.read_lines(lines)

    def read_lines(self, lines):
        # Keep track of parents of nested lines, with a tuple of id and tier
        # Refreshes if tier is the same, pushes if higher, pops if lower.
        stack = ParentStack()
        current_section = ""
        for line in lines:
            line_type = line.pop(0)
            trimmed = re.subn(r'\t','',line_type)
            try:
                obj = self.typenames[trimmed[0]](line, trimmed[1])
            except (KeyError) as e:
                print(f'Line: [{line_type + " " +" ".join(line)}] not recognised')
                continue
            if isinstance(obj, ListItem):
                obj.parent = stack.compare((obj.id, obj.indent))
                print(obj.parent)
                if obj.parent:
                    obj.parent = self.listitems[obj.parent]
                    obj.parent.attach(obj)
                obj.section = current_section
                while obj.id in self.listitems.keys():
                    obj.id = obj.id + 1
                self.listitems[obj.id] = obj   
            if isinstance(obj, SectionHeader):
                current_section = re.sub(r'[:\s]','',obj.text.lower())

class Merger:
    def __init__(self, db_tasks, pulled_tasks):
        self.db_tasks = db_tasks
        self.p_tasks = pulled_tasks
        self.conflicts = []
        self.ids = set(pulled_tasks.keys())
    
    def merge_pull(self):
        for task in self.db_tasks:
            if task['id'] not in self.p_tasks.keys():
                self.p_tasks[task['id']] = task
                self.ids.add(task['id'])
                continue
            if self.p_tasks[task['id']].is_same_as(task):
                continue
            else:
                self.conflicts.append(task)
        print(f"Merged with {len(self.conflicts)} conflict(s)")
        self.resolve_conflicts()
        new = self.build_tasks()
        return new

    def build_tasks(self):
        newtasks = []
        print(self.p_tasks)
        for value in self.p_tasks.values():
            if isinstance(value, ListItem):
                newtasks.append(value.as_json())
            else:
                newtasks.append(value)
        return newtasks

    
    def resolve_conflicts(self):
        for conflict in self.conflicts:
            self.print_conflict(conflict, self.p_tasks[conflict['id']])
            while True:
                user_choice = input("Please enter a choice:")
                if user_choice == '1':
                    self.reallocate(self.p_tasks[conflict['id']])
                    self.p_tasks[conflict['id']] = conflict
                    break
                elif user_choice == '2':
                    break
                elif user_choice == '3':
                    self.p_tasks[conflict['id']] = conflict
                    break
            del conflict

    def reallocate(self, task):
        new_task_id = 1
        while new_task_id in self.ids:
            new_task_id = new_task_id + 1
        task.id = new_task_id
        self.p_tasks[new_task_id] = task
        self.ids.add(new_task_id)


    def print_conflict(self, existing, new):
        id = existing['id']
        text = existing['description']
        print(f'Conflict was found between existing [{id}] and pulled [{new.id}]:')
        print(f'Existing: [{id}] - {text}')
        print(f'Pulled: [{new.id}] - {new.text}')
        print("Would you like to: \n1. Save pulled with new id\n2. Overwrite existing\n3. Discard pulled")


class ParentStack:
    """
    Keep track of parents of nested lines, with a tuple of id and tier
    Refreshes if tier is the same, pushes if higher, pops if lower.
    """
    def __init__(self):
        self.stack = []

    def isempty(self):
        if len(self.stack) == 0:
            return True
        return False
    
    def push(self, item):
        self.stack.append(item)
    
    def compare(self, item):
        if not self.isempty():
            top = self.stack.pop(-1)
            if top[1] > item[1]:
                self.compare(item)
            elif top[1] < item[1]:
                self.push(top)
                self.push(item)
            else:
                self.push(item)
            if len(self.stack) > 1:
                return self.stack[-2][0]
        else:
            self.push(item)
        return None
            


class ProjectHeader:
    def __init__(self, contents, _):
        self.text = re.sub(r'\n', '', " ".join(contents))
    
    def as_string(self):
        return f"Project: {self.text}"

class SectionHeader:
    def __init__(self, contents, _):
        self.contents = contents
        self.text = re.sub(r'\n', '', ' '.join(contents))
     
    def as_string(self):
        return f"Section: {self.text}"


class ListItem:
    def __init__(self, contents, indent):
        self.contents = contents
        self.parent = None
        self.id = int(re.sub(r'[\[\]\:]', '', contents[0]))
        self.text = re.sub(r'\n', '', contents[1])
        self.indent = indent
        self.section = ""
        self.children = []
        self.DEV_children_string = ""
        self.DEV_parent_string = ''
    
    def attach(self, item):
        self.children.append(item)
        self.DEV_children_string = self.DEV_make_children_string()
   
    def DEV_make_children_string(self):
        string = " [Children: "
        for child in self.children:
            string = string + str(child.id) + " "
        string = string + "]"
        return string
    
    def is_same_as(self, other):
        this = {
            "id":self.id,
            "description":self.text,
        }
        for key in this.keys():
            if isinstance(other[key],list):
                if set(this[key]) != set(other[key]):
                    return False
            elif this[key] != other[key]:
                return False
        return True
    
    def as_json(self):
        children_ids = []
        for child in self.children:
            children_ids.append(child.id)
        if self.parent:
            parent_id = self.parent.id
        else:
            parent_id = []
        return dict({
            "id":self.id,
            "description":self.text,
            "status": self.section,
            "priority":1,
            "children":children_ids,
            "parent": parent_id
        })



    def as_string(self):
        return f"{self.section}: {self.id} - {self.text}{self.DEV_children_string}"
   