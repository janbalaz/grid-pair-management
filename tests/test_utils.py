import pytest
import backend.utils as utils

counts = [10, 100, 62, 13, 80]


@pytest.mark.parametrize("count", counts)
def test_object_generator(count):
    assert len(utils.generate_objects(count, 1000, 1000, 100, 100)) == count