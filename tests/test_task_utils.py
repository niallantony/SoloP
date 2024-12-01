from unittest.mock import patch
import pytest
from project_plan_manager.task_utils import (
    Task,
    add_task, 
    delete_task, 
    change_status, 
    get_task, 
    get_of_status,
    get_status_list,
    as_task_object,
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

def test_add_task_with_newline():
    with pytest.raises(InvalidTaskError):
        add_task(mock_data, "Task with new line \n")

def test_delete_task():
    task_id = mock_data[0]['id']
    modified_tasks = delete_task(mock_data, task_id)
    assert task_id not in [task['id'] for task in modified_tasks]

def test_cannot_delete_missing_task():
    with pytest.raises(StopIteration):
        delete_task([],1)
    
@pytest.mark.parametrize("new, expected", 
    [
        pytest.param("in_progress", "in_progress", id="changes simple"),
        pytest.param("Done", "done", id="change is case insensitive"),
        pytest.param("in progress", "in_progress", id="deals with whitespace"),
    ]
)
def test_change_status(new, expected):
    modified_tasks = change_status(mock_data.copy(), 1, new) 
    assert modified_tasks[0]['status'] == expected


def test_cannot_change_status_missing_task():
    with pytest.raises(StopIteration):
        change_status(mock_data,2,"in_progress")

def test_get_task():
    task = get_task(mock_data,1)
    assert task.description == "Existing Task"
    assert type(task) is Task

def test_get_task_throws_missing_task():
    with pytest.raises(StopIteration):
        task = get_task(mock_data, 2)

def test_get_of_status():
    backlog = get_of_status(mock_data_extended, "backlog")
    assert type(backlog) is list
    assert len(backlog) == 2
    assert type(backlog[0]) is Task

def test_get_of_status_no_status():
    empty_list = get_of_status([{"id":1, "description":"Test Task"}], "backlog")
    assert len(empty_list) == 0
        
@pytest.mark.parametrize("values,length,expected",
    [
        pytest.param([{"status":"backlog"}], 1, ["backlog"], id="one item"),
        pytest.param([{"status":"backlog"}, {"status":"backlog"},{"status":"backlog"}], 1, ["backlog"], id="three items, same status"),
        pytest.param([{"status":"backlog"},{"status":"done"},{"status":"done"}], 2, ["backlog","done"], id="three items, two statuses"),
    ]
)
def test_get_status_list(values,length,expected):
    statuses = get_status_list(values)
    assert len(statuses) == length
    assert statuses == expected


def test_as_task_object():
    task_object = as_task_object({"id":1, "description": "Test Task","status":"backlog"})
    assert type(task_object) is Task

def test_as_task_object_no_id():
    with pytest.raises(KeyError):
        task_object = as_task_object({"description": "Test Task","status":"backlog"})

def test_as_task_object_no_description():
    with pytest.raises(KeyError):
        task_object = as_task_object({"id":1,"status":"backlog"})

def test_as_task_object_no_status():
    task_object = as_task_object({"id":1,"description": "Test Task"})
    assert type(task_object) is Task
    assert task_object.status == "backlog"
        
def test_task_as_string():
    task_object = Task(id=1, description="Test Task")
    assert task_object.as_string() == "- [1]: Test Task"

