import pytest
from backend.box import Box

coordinates = [([(10, 10), (115, 12), (56, 14), (0, 180), (50, 0)], [0, 0, 115, 180]),
               ([(10, 5)], [10, 5, 10, 5]),
               ([(112, 192), (1150, 1), (185, 16), (92, 136)], [92, 1, 1150, 192]),
               ([(99, 99), (99, 99), (99, 99)], [99, 99, 99, 99]),
               ([(121, 170), (15, 12), (576, 140), (50, 987), (333, 666), (156, 123)], [15, 12, 576, 987])]


@pytest.mark.parametrize("coordinates, expected", coordinates)
def test_box_create_aabb(coordinates, expected):
    box = Box(1, coordinates)
    assert box.min_x == expected[0]
    assert box.min_y == expected[1]
    assert box.max_x == expected[2]
    assert box.max_y == expected[3]
