"""Contains various helper functions for other modules."""
import random
import json
from backend.box import Box
from enum import Enum
from collections import OrderedDict


class StoreType(Enum):
    matrix = "matrix"
    hashed = "hashed"


def generate_objects(count, x_size, y_size, max_x_size, max_y_size, cell_size):
    """Generates random sized and placed objects."""
    objects = []
    x_limit = x_size-cell_size
    y_limit = y_size-cell_size
    for i in range(count):
        start_x = random.randrange(0, x_limit, 1)
        start_y = random.randrange(0, y_limit, 1)
        nodes_count = random.randrange(3, 10, 1)
        points = []
        while len(points) < nodes_count:
            x = random.randrange(-max_x_size, max_x_size, 1)
            y = random.randrange(-max_y_size, max_y_size, 1)
            x = start_x + x
            y = start_y + y
            if 0 <= x < x_limit and 0 <= y < y_limit:
                points.append((x, y))

        dx = random.randint(cell_size/2 + 1, cell_size)
        dy = random.randint(cell_size/2 + 1, cell_size)

        objects.append(Box(i, points, dx, dy))

    return objects


def parse_grid(grid):
    """Creates dict dump from dense matrix. Used for JSON dump."""
    parsed = OrderedDict()
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(grid)
    for i in range(len(grid)):
        #print("i: {}".format(i))
        parsed[str(i)] = OrderedDict()
        for j in range(len(grid[i])):
            #print("j: {}".format(j))
            parsed[str(i)][str(j)] = [x for x in grid[i][j].ids]
    return parsed


def get_grids_json(grid_managers, boxes, times=None):
    """Collects grids from grid managers and returns them in single JSON."""
    if times is None:
        times = []
    grids = {}
    for key, gm in grid_managers.items():
        grids[key] = parse_grid(gm.grid)

    grids["boxes"] = []
    grids["objects"] = []
    for box in boxes:
        grids["boxes"].append([box.min_x, box.min_y, box.max_x, box.max_y])
        grids["objects"].append(box.coordinates)

    grids["times"] = times
    return json.dumps(grids)

if __name__ == "__main__":
    pass
