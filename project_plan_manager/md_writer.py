from project_plan_manager.task_utils import (
    get_of_status,
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
            writer.write(self.__br())
            backlog = self.format_list_with_header(self.backlog_tasks, "backlog")
            for line in backlog:
                writer.write(line)

    def format_list_with_header(self, items, header):
        output = [(self.as_header(header, 2) + ': \n\n')]
        output = output + self.format_as_list(items)
        return output
    
    def format_as_list(self, items):
        output = []
        for item in items:
            output.append(item.as_string() + '\n')
        return output

    def __br(self):
        return "\n"
        
    def as_header(self, header, level=1):
        output = ""
        for x in range(level):
            output = output + "#"
        output = output + " " + header.upper()
        return output
