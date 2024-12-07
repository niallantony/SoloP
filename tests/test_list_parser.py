import copy
import pytest
from unittest.mock import patch
from solop.list_parser import ListItem, ListParser, Merger

mock_lines = [
    "# PROJECT\n",
    "\n",
    "## BACKLOG:\n",
    "\n",
    "- [1]: Item one\n",
    "- [2]: Item two\n",
    "\t- [3]: Nested item one\n",
    "\t- [4]: Nested item two\n",
    "\t\t- [5]: Double nested item\n",
]

mock_json = {
    "id": 1,
    "description": "Item one",
    "status": "backlog",
    "priority": 1,
    "children": [],
    "parent": []
}

def test_list_item_equality_correct():
    correct = ListItem(['1', 'Item one'], 1)
    correct.section = "backlog"
    assert correct.is_same_as(mock_json)

@pytest.mark.parametrize(["given"], [
    pytest.param(ListItem(['2', 'Item one'], 1), id="differing id"),
    pytest.param(ListItem(['1', 'Item two'], 1), id="differing text")
])
def test_list_items_equality_incorrect(given):
    assert not given.is_same_as(mock_json)

def test_read_items():
    parser = ListParser()
    lines = [['#','PROJECT'],['##','BACKLOG:'],['-','[1]:','Task one'],['-','[2]:','Task two']]
    parser.read_lines(lines)
    assert len(parser.listitems.keys()) == 2
    assert isinstance(parser.listitems[1], ListItem)
    assert parser.listitems[1].as_string() == "backlog : 1 - Task one"
    
def test_list_items_duplicate_id():
    parser = ListParser()
    lines = [['-','[1]:','Task one'],['-','[1]:','Task two']]
    parser.read_lines(lines)
    assert 2 in parser.listitems.keys()
    assert parser.listitems[2].text == 'Task two'

@pytest.mark.parametrize(["item", "conflicts"], [
    pytest.param({2:ListItem(['2', 'Item two'], 1)}, 0, id="two distinct ids"),
    pytest.param({1:ListItem(['1', 'Item two'], 1)}, 1, id="same id, different text"),
    pytest.param({1:ListItem(['1', 'Item one'], 1)}, 0, id="same items")
])
def test_merger_conflicts(item, conflicts):
    merger = Merger([copy.deepcopy(mock_json)], item)
    merger.merge_pull()
    merger.resolve_conflicts()
    assert len(merger.conflicts) != conflicts