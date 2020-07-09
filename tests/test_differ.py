from copy import deepcopy

from data_diff.differ import Differ
from tests._fakes import FakeLoader


base = {
    "col1": ["a", "b", "c", "d"],
    "col2": [1, 2, 3, 4]
}

append_lines = {
    "col1": ["a", "b", "c", "d", "e"],
    "col2": [1, 2, 3, 4, 5]
}

delete_lines = {
    "col1": ["a", "b", "d"],
    "col2": [1, 2, 4]
}

update_lines = {
    "col1": ["a", "b", "d", "c"],
    "col2": [1, 2, 4, 5]
}


dataset1 = (deepcopy(base), append_lines, delete_lines, update_lines)
dataset2 = (deepcopy(base), deepcopy(base), deepcopy(base), deepcopy(base))


def test_differ():
    differ = Differ(FakeLoader(dataset1), FakeLoader(dataset2))
    differ.auto_differences()

    for index, data in enumerate(zip(dataset1, dataset2)):
        frame1, frame2 = data
        assert frame1 == frame2, f"Frames not equals at index: {index}"
