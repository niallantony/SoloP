from unittest.mock import mock_open, patch
import pytest
import json
import sys
import os
from project_plan_manager.plan_manager import load_tasks, save_tasks, add_task, delete_task, InvalidTaskError

mock_data = [{
    "id":1,
    "description": "Existing Task"
}]

def mock_json_data():
    return json.dumps(mock_data)

def test_load_tasks():
    with patch("builtins.open", mock_open(read_data=mock_json_data())):
        tasks = load_tasks()
        assert tasks == mock_data

def test_save_tasks():
    with patch("builtins.open", mock_open()) as mock_file:
        save_tasks(mock_data)
        written_data = "".join(call.args[0] for call in mock_file().write.call_args_list)
        assert written_data == json.dumps(mock_data, indent=4)

def test_add_task():
    mock_tasks = [{"id":1, "description":"Mock Task"}]
    with patch("project_plan_manager.plan_manager.load_tasks", side_effect=lambda: mock_tasks.copy()), \
         patch("project_plan_manager.plan_manager.save_tasks", side_effect=lambda tasks: (mock_tasks.clear(), mock_tasks.extend(tasks))):
        add_task("Test Task")
        assert len(mock_tasks) == 2
        assert mock_tasks[-1]['description'] == "Test Task"

def test_cannot_add_empty_description_task():
    with patch("project_plan_manager.plan_manager.load_tasks", return_value=[]), \
         pytest.raises(InvalidTaskError):
        add_task("")
        
def test_cannot_add_null_task():
    with patch("project_plan_manager.plan_manager.load_tasks", return_value=[]), pytest.raises(AssertionError):
        add_task(None)
    
def test_added_tasks_default_to_backlog():
    mock_tasks = []
    with patch("project_plan_manager.plan_manager.load_tasks", side_effect=lambda: mock_tasks.copy()), \
         patch("project_plan_manager.plan_manager.save_tasks", side_effect=lambda tasks: (mock_tasks.clear(), mock_tasks.extend(tasks))):
        add_task("Test Task")
        assert mock_tasks[-1]['status'] == "backlog"


def test_delete_task():
    mock_tasks = [{"id":1, "description":"Mock Task"}]
    with patch("project_plan_manager.plan_manager.load_tasks", side_effect=lambda: mock_tasks), \
         patch("project_plan_manager.plan_manager.save_tasks", side_effect=lambda tasks: (mock_tasks.clear(), mock_tasks.extend(tasks))):
        task_id = mock_tasks[0]['id']
        delete_task(task_id)
        assert task_id not in [task['id'] for task in mock_tasks]

def test_cannot_delete_missing_task():
    with patch("project_plan_manager.plan_manager.load_tasks", return_value=[]), \
         pytest.raises(StopIteration):
        delete_task(1)