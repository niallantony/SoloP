from unittest.mock import mock_open, patch
import json
from project_plan_manager.file_utils import(
    load_tasks,
    save_tasks,
)

mock_data = [
{
    "id":1,
    "description": "Existing Task",
    "status": "backlog"
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

