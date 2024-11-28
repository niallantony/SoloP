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
    modified_tasks = add_task(mock_data,"Test Task")
    assert len(modified_tasks) == 2
    assert modified_tasks[-1]['description'] == "Test Task"

def test_cannot_add_empty_description_task():
    with pytest.raises(InvalidTaskError):
        add_task(mock_data,"")
        
def test_cannot_add_null_task():
    with pytest.raises(AssertionError):
        add_task(mock_data,None)
    
def test_added_tasks_default_to_backlog():
    modified_tasks = add_task(mock_data, "Test Task")
    assert modified_tasks[-1]['status'] == "backlog"


def test_delete_task():
    task_id = mock_data[0]['id']
    modified_tasks = delete_task(mock_data, task_id)
    assert task_id not in [task['id'] for task in modified_tasks]

def test_cannot_delete_missing_task():
    with pytest.raises(StopIteration):
        delete_task([],1)