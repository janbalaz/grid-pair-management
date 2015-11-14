"""Contains various helper functions for other modules."""
import random
import json
from box import Box
from enum import Enum
from collections import OrderedDict
MNGMT_TYPE = Enum('MNGMT_TYPE', 'matrix hashed')


def hash_bids(n, bid1, bid2):
    """Returns hash of a pair limited by the count of objects."""
    prime1 = 15485863
    prime2 = 32452843
    return (bid1*prime1 ^ bid2*prime2) % n


def generate_objects(count, x_size, y_size, max_x_size, max_y_size):
    """Generates random sized and placed objects."""
    objects = []
    for i in range(count):
        start_x = random.randrange(0, x_size, 1)
        start_y = random.randrange(0, y_size, 1)
        nodes_count = random.randrange(3, 10, 1)
        points = []
        while len(points) < nodes_count:
            x = random.randrange(-max_x_size, max_x_size, 1)
            y = random.randrange(-max_y_size, max_y_size, 1)
            x = start_x + x
            y = start_y + y
            if 0 <= x <= x_size and 0 <= y <= y_size:
                points.append((x, y))

        objects.append(Box(i, points))

    return objects


def parse_grid(grid):
    """Creates dict dump from dense matrix. Used for JSON dump."""
    parsed = OrderedDict()
    for i in range(len(grid)):
        parsed[str(i)] = OrderedDict()
        for j in range(len(grid)):
            parsed[str(i)][str(j)] = [x for x in grid[i][j].ids]
    return parsed


def get_grids_json(grid_managers, times=[]):
    """Collects grids from grid managers and returns them in single JSON."""
    grids = {}
    for key, gm in grid_managers.iteritems():
        grids[key] = parse_grid(gm.grid)

    grids["times"] = times
    return json.dumps(grids)

if __name__ == "__main__":
    pass
