from unittest.mock import  patch
import pytest
import json
from project_plan_manager.file_utils import(
    load_tasks,
    save_tasks,
    change_meta,
    InvalidAttrError
)

mock_data = {
"project":"Name",
"tasks":{
    "id":1,
    "description": "Existing Task",
    "status": "backlog"
}
}

mock_tasks = {
    "id":2,
    "description":"New Task",
    "status": "in_progress"
}

def mock_json_data():
    return json.dumps(mock_data)

def test_load_tasks():
    with patch("project_plan_manager.file_utils.load_file", return_value=mock_data.copy()):
        tasks = load_tasks()
        assert tasks == mock_data["tasks"]

def test_save_tasks():
    with patch("project_plan_manager.file_utils.load_file", return_value=mock_data.copy()), \
        patch("project_plan_manager.file_utils.save_file") as mock_save_file:
        save_tasks(mock_tasks)
        expected = {
            "project":"Name",
            "tasks": mock_tasks
        }
        mock_save_file.assert_called_once_with(expected)
        mock_save_file.reset_mock()

def test_change_meta_name():
    with patch("project_plan_manager.file_utils.load_file", return_value=mock_data.copy()), \
        patch("project_plan_manager.file_utils.save_file") as mock_save_file:
        change_meta('project','New Name')
        args, kwargs = mock_save_file.call_args
        assert args[0]['project'] == "New Name"
        mock_save_file.reset_mock()

def test_change_meta_not_existing():
    with patch("project_plan_manager.file_utils.load_file", return_value=mock_data), \
        pytest.raises(InvalidAttrError):
        change_meta('foo','bar')


   