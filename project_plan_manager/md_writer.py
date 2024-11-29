from task_utils import (
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
            backlog = self.list_with_header(self.backlog_tasks, "backlog")
            for line in backlog:
                writer.write(line)


    def list_with_header(self, tasks, header):
        output = [(self.as_header(header, 2) + ":")]
        output.append(self.__br())
        for task in tasks:
            output.append(task.as_string())
        return output
    
    def __br(self):
        return "\n"
        
    def as_header(self, header, level=1):
        output = ""
        for x in range(level):
            output = output + "#"
        output = output + " " + header.upper()
        return output
