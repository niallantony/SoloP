from unittest.mock import patch
import pytest
from project_plan_manager.task_utils import (
    add_task, 
    delete_task, 
    change_status, 
    get_task, 
    get_of_status,
    InvalidTaskError,
)

mock_data = [
{
    "id":1,
    "description": "Existing Task",
    "status": "backlog"
}]

mock_data_extended = [
{
    "id":1,
    "description":"Backlog 1",
    "status": "backlog"
},
{
    "id":2,
    "description":"Backlog 2",
    "status": "backlog"
},
{
    "id":3,
    "description":"Progress 2",
    "status": "in_progress"
}]

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
    
def test_change_status():
    modified_tasks = change_status(mock_data, 1, "in_progress") 
    assert modified_tasks[0]['status'] == "in_progress"

def test_cannot_change_status_missing_task():
    with pytest.raises(StopIteration):
        change_status(mock_data,2,"in_progress")

def test_get_task():
    with patch("project_plan_manager.task_utils.load_tasks", return_value = mock_data.copy()):
        task = get_task(1)
        assert task['description'] == "Existing Task"

def test_get_test_throws_missing_test():
    with patch("project_plan_manager.task_utils.load_tasks", return_value=mock_data.copy()), \
    pytest.raises(StopIteration):
        task = get_task(2)

def test_get_of_status():
    with patch("project_plan_manager.task_utils.load_tasks", return_value=mock_data_extended.copy()):
        backlog = get_of_status("backlog")
        assert type(backlog) is list
        assert len(backlog) == 2
        
