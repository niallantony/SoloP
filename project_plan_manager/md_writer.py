import re
from project_plan_manager.task_utils import (
    get_of_status,
    sort_tasks,
    get_status_list,
    as_task_object,
)

class MDWriter:
    def __init__(self, name, tasks):
        self.name = name
        self.tasks = tasks
        self.backlog_tasks = get_of_status(tasks, "backlog")
        self.in_progress_tasks = get_of_status(tasks, "in_progress")
        self.done_tasks = get_of_status(tasks, "done")

    def write_md_file(self):
        with open('SOLOP.md', 'w') as writer:
            writer.write(self.as_header(self.name))
            writer.write(self.__br(2))
            statuses = get_status_list(self.tasks)
            for status in statuses:
                lines = self.format_section(status)
                writer.writelines(lines)
            writer.write("This document was generated with SoloP")
    
    def format_section(self, status):
        lines = []
        tasks = get_of_status(self.tasks, status)
        tasks = sort_tasks(tasks, "priority")
        section = self.format_list_with_header(tasks, status)
        for line in section:
            lines.append(line)
        lines.append(self.__br(1))
        return lines

    def format_list_with_header(self, items, header):
        output = [(self.as_header(header, 2) + ': \n\n')]
        output = output + self.format_as_list(items)
        return output
    
    def format_as_list(self, items):
        output = []
        for item in items:
            item = as_task_object(item)
            output.append(item.as_string() + '\n')
        return output

    def __br(self, number):
        output = ""
        for n in range(number):
            output = output + "\n"
        return output
        
    def as_header(self, header, level=1):
        output = ""
        for x in range(level):
            output = output + "#"
        header = re.sub(r"_", " ", header)
        output = output + " " + header.upper()
        return output
