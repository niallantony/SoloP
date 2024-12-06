import re

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
        # Keep track of parents of nested lines, with a tuple of id and tier
        # Refreshes if tier is the same, pushes if higher, pops if lower.
        stack = ParentStack()
        current_section = ""
        for line in lines:
            line_type = line.pop(0)
            trimmed = re.subn(r'\t','',line_type)
            obj = self.typenames[trimmed[0]](line, trimmed[1])
            if isinstance(obj, ListItem):
                obj.parent = stack.compare((obj.id, obj.indent))
                if obj.parent:
                    self.listitems[obj.parent].attach(obj)
                obj.section = current_section
                self.listitems[obj.id] = obj   
            if isinstance(obj, SectionHeader):
                current_section = obj.text
    
        for item in self.listitems:
            print(self.listitems[item].as_string())


class ParentStack:
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
        self.children_string = ""
    
    def attach(self, item):
        self.children.append(item)
        self.children_string = self.make_children_string()
   
    def make_children_string(self):
        string = "[Children: "
        for child in self.children:
            string = string + str(child.id) + " "
        string = string + "]"
        return string
    
    def as_string(self):
        return f"{self.section}: {self.id} - {self.text} (With parent: {self.parent}) {self.children_string}"

