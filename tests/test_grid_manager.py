import pytest
from backend.grid_manager import Cell, GridManager, StoreType
from backend.box import Box

# python -m pytest C:\Users\johny\PycharmProjects\grid-pair-management\tests\test_grid_manager.py

cell_init_data = [(StoreType.matrix, 42),
                  (StoreType.hashed, 123)]

# TODO: add only first object
cell_add_pairs = [(StoreType.hashed, 42, {1, 3, 5}, {(1, 3), (3, 1), (1, 5), (5, 1), (3, 5), (5, 3)}, 6,
                   {(1, 3), (3, 1), (1, 5), (5, 1), (3, 5), (5, 3), (1, 6), (6, 1), (3, 6), (6, 3), (5, 6), (6, 5)}),
                  (StoreType.hashed, 42, {2, 4}, {(2, 4), (4, 2)}, 6,
                   {(2, 4), (4, 2), (2, 6), (6, 2), (4, 6), (6, 4)}),
                  (StoreType.matrix, 3, {0, 2}, [[False, False, True], [False, False, False], [True, False, False]],
                   1, [[False, True, True], [True, False, True], [True, True, False]]),
                  (StoreType.matrix, 2, {0}, [[False, False], [False, False]], 1,
                   [[False, True], [True, False]])]

cell_remove_pairs = [(StoreType.hashed, 42, {1, 3, 5}, {(1, 3), (3, 1), (1, 5), (5, 1), (3, 5), (5, 3)}, 3,
                      {(1, 5), (5, 1)}),
                     (StoreType.hashed, 42, {2, 4}, {(2, 4), (4, 2)}, 2, set()),
                     (StoreType.matrix, 3, {0, 1, 2}, [[False, True, True], [True, False, True], [True, True, False]],
                      1, [[False, False, True], [False, False, False], [True, False, False]]),
                     (StoreType.matrix, 2, {0, 1}, [[False, True], [True, False]], 1,
                      [[False, False], [False, False]])]

grid_init_data = [(StoreType.matrix, 10, 600, 600, 100, 6, 6),
                  (StoreType.hashed, 5, 300, 300, 50, 6, 6),
                  (StoreType.matrix, 10, 1000, 600, 100, 10, 6),
                  (StoreType.hashed, 10, 300, 600, 25, 12, 24),
                  (StoreType.matrix, 10, 1000, 600, 0, 0, 0),
                  (StoreType.matrix, 10, 1000, 0, 100, 10, 0),
                  (StoreType.matrix, 10, 0, 600, 100, 0, 6)]

grid_cell_data = [(100, 200, 25, 4, 8),
                  (100, 200, 9, 11, 22),
                  (100, 200, 8, 12, 25),
                  (100, 200, 0, 0, 0),
                  (0, 200, 10, 0, 20),
                  (100, 0, 10, 10, 0)]

grid_add_box_data = [
    (Box(1, [(0, 0), (400, 400), (0, 400), (400, 0)]), 0, 8, 0, 8),
    (Box(1, [(50, 0), (100, 0), (200, 52), (50, 580), (100, 512), (242, 300)]), 1, 4, 0, 11)]


@pytest.mark.parametrize("store_type, obj_count", cell_init_data)
def test_cell_init(store_type, obj_count):
    cell = Cell(store_type, obj_count)
    assert cell.count == obj_count
    assert cell.store_type == store_type

    if store_type == StoreType.matrix:
        assert isinstance(cell.pairs, list)
    else:
        assert isinstance(cell.pairs, set)


@pytest.mark.parametrize("store_type, obj_count, ids, pairs, bid, exp_pairs", cell_add_pairs)
def test_cell_add_pairs(store_type, obj_count, ids, pairs, bid, exp_pairs):
    cell = Cell(store_type, obj_count)
    cell.ids = ids
    cell.pairs = pairs
    cell.add_pairs(bid)

    my_ids = set(ids)
    my_ids.add(bid)
    assert cell.ids == my_ids
    assert cell.pairs == exp_pairs


@pytest.mark.parametrize("store_type, obj_count, ids, pairs, bid, exp_pairs", cell_remove_pairs)
def test_cell_remove_pairs(store_type, obj_count, ids, pairs, bid, exp_pairs):
    cell = Cell(store_type, obj_count)
    cell.ids = ids
    cell.pairs = pairs
    cell.remove_pairs(bid)

    my_ids = set(ids)
    my_ids.discard(bid)
    assert cell.ids == my_ids
    assert cell.pairs == exp_pairs


@pytest.mark.parametrize("store_type, obj_count, x_size, y_size, cell_size, exp_x, exp_y", grid_init_data)
def test_grid_manager_init(store_type, obj_count, x_size, y_size, cell_size, exp_x, exp_y):
    gm = GridManager(store_type, obj_count, x_size, y_size, cell_size)

    assert gm.cell_size == cell_size
    assert len(gm.grid) == exp_x
    if exp_x and exp_y:
        assert len(gm.grid[0]) == exp_y
        assert isinstance(gm.grid[0][0], Cell)
    else:
        assert exp_x == 0 or exp_y == 0


@pytest.mark.parametrize("x, y, cell_size, exp_x, exp_y", grid_cell_data)
def test_grid_manager_cell_coordinates(x, y, cell_size, exp_x, exp_y):
    gm = GridManager(x_size=x, y_size=y, cell_size=cell_size)
    assert gm._cell(x, y) == (exp_x, exp_y)


@pytest.mark.parametrize("box, min_x, max_x, min_y, max_y", grid_add_box_data)
def test_grid_manager_add_box(box, min_x, max_x, min_y, max_y):
    gm1 = GridManager(x_size=600, y_size=600, cell_size=50)
    gm2 = GridManager(store_type=StoreType.hashed, x_size=600, y_size=600, cell_size=50)

    gm1.add_box(box)
    gm2.add_box(box)

    for i in range(min_x, max_x + 1):
        for j in range(min_y, max_y + 1):
            assert box.bid in gm1.grid[i][j].ids
            assert box.bid in gm2.grid[i][j].ids


grid_add_boxes_data = [()]


@pytest.mark.parametrize("boxes, min_x, max_x, min_y, max_y, exp_pairs", grid_add_boxes_data)
def test_grid_manager_add_boxes_to_matrix(boxes, min_x, max_x, min_y, max_y, exp_pairs):
    gm1 = GridManager(x_size=600, y_size=600, cell_size=50)
    #gm2 = GridManager(store_type=StoreType.hashed, x_size=600, y_size=600, cell_size=50)

    for box in boxes:
        gm1.add_box(box)

    for i in range(min_x, max_x + 1):
        for j in range(min_y, max_y + 1):
            assert box.bid in gm1.grid[i][j].ids
            #assert box.bid in gm2.grid[i][j].ids