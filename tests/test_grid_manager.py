import pytest
from backend.grid_manager import Cell, GridManager, MNGMT_TYPE

cell_init_data = [(MNGMT_TYPE.matrix, 42),
                  (MNGMT_TYPE.hashed, 123)]

# TODO: add only first object
cell_add_pairs = [(MNGMT_TYPE.hashed, 42, {1, 3, 5}, {(1, 3), (3, 1), (1, 5), (5, 1), (3, 5), (5, 3)}, 6,
                  {(1, 3), (3, 1), (1, 5), (5, 1), (3, 5), (5, 3), (1, 6), (6, 1), (3, 6), (6, 3), (5, 6), (6, 5)}),
                  (MNGMT_TYPE.hashed, 42, {2, 4}, {(2, 4), (4, 2)}, 6,
                  {(2, 4), (4, 2), (2, 6), (6, 2), (4, 6), (6, 4)}),
                  (MNGMT_TYPE.matrix, 3, {0, 2}, [[False, False, True], [False, False, False], [True, False, False]],
                  1, [[False, True, True], [True, False, True], [True, True, False]]),
                  (MNGMT_TYPE.matrix, 2, {0}, [[False, False], [False, False]], 1,
                  [[False, True], [True, False]])]

cell_remove_pairs = [(MNGMT_TYPE.hashed, 42, {1, 3, 5}, {(1, 3), (3, 1), (1, 5), (5, 1), (3, 5), (5, 3)}, 3,
                      {(1, 5), (5, 1)}),
                     (MNGMT_TYPE.hashed, 42, {2, 4}, {(2, 4), (4, 2)}, 2, set()),
                     (MNGMT_TYPE.matrix, 3, {0, 1, 2}, [[False, True, True], [True, False, True], [True, True, False]],
                      1, [[False, False, True], [False, False, False], [True, False, False]]),
                     (MNGMT_TYPE.matrix, 2, {0, 1}, [[False, True], [True, False]], 1,
                      [[False, False], [False, False]])]


@pytest.mark.parametrize("mngmt_type, obj_count", cell_init_data)
def test_cell_init(mngmt_type, obj_count):
    cell = Cell(mngmt_type, obj_count)
    assert cell.count == obj_count
    assert cell.mngmt_type == mngmt_type

    if mngmt_type == MNGMT_TYPE.matrix:
        assert isinstance(cell.pairs, list)
    else:
        assert isinstance(cell.pairs, set)


@pytest.mark.parametrize("mngmt_type, obj_count, ids, pairs, bid, exp_pairs", cell_add_pairs)
def test_cell_add_pairs(mngmt_type, obj_count, ids, pairs, bid, exp_pairs):
    cell = Cell(mngmt_type, obj_count)
    cell.ids = ids
    cell.pairs = pairs
    cell.add_pairs(bid)

    my_ids = set(ids)
    my_ids.add(bid)
    assert cell.ids == my_ids
    assert cell.pairs == exp_pairs


@pytest.mark.parametrize("mngmt_type, obj_count, ids, pairs, bid, exp_pairs", cell_remove_pairs)
def test_cell_remove_pairs(mngmt_type, obj_count, ids, pairs, bid, exp_pairs):
    cell = Cell(mngmt_type, obj_count)
    cell.ids = ids
    cell.pairs = pairs
    cell.remove_pairs(bid)

    my_ids = set(ids)
    my_ids.discard(bid)
    assert cell.ids == my_ids
    assert cell.pairs == exp_pairs

