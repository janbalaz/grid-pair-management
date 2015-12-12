import pytest
import backend.utils as utils

# python -m pytest C:\Users\johny\PycharmProjects\grid-pair-management\tests\test_utils.py

counts = [10, 100, 62, 13, 80]


@pytest.mark.parametrize("count", counts)
def test_object_generator(count):
    assert len(utils.generate_objects(count, 1000, 1000, 100, 100)) == count


def test_parse_grid():
    pass


def test_parse_grid():
    pass
