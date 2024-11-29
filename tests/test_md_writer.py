import pytest
from unittest.mock import patch

from project_plan_manager.task_utils import (
    Task,
)

from project_plan_manager.md_writer import (
    MDWriter,
)

def new_as_string():
    return "- [1]: Test Task"


mock_list = [
    {
        "id":1,
        "description":"Task 1",
        "status":"backlog"
    },
    {
        "id":2,
        "description":"Task 2",
        "status":"backlog"
    }
    ]

def test_list_section_with_header():
    writer = MDWriter("Project", mock_list) 
    section_list = writer.format_list_with_header(writer.backlog_tasks,"backlog")
    assert len(section_list) == 3
    assert section_list[0] == "## BACKLOG: \n\n"