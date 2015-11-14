import sys
import math
from box import Box
from utils import MNGMT_TYPE, hash_bids


class Cell:
    """This class represents single cell in grid (dense matrix).
    It implements methods for adding and removing pairs.
    """

    def __init__(self, mngmt_type, obj_count=0):
        """Based on management type creates dense matrix (as lists in list in Python)
        or dict with set as a bucket (in case there is a collision in hashing).
        Object count is used for hash computation.
        """
        self.mngmt_type = mngmt_type
        self.count = obj_count
        self.ids = set()

        if self.mngmt_type == MNGMT_TYPE.matrix:
            self.pairs = [[False for y in range(self.count)] for x in range(self.count)]
        else:
            self.pairs = dict()

    def add_pairs(self, bid):
        """Adds new pairs with new object with box ID. Addition is based on management type."""
        if self.mngmt_type == MNGMT_TYPE.matrix:
            for bid2 in self.ids:
                self.pairs[bid][bid2] = True
                self.pairs[bid2][bid] = True
        else:
            for bid2 in self.ids:
                key = hash_bids(self.count, bid, bid2)
                bucket = self.pairs.setdefault(key, set())
                bucket.add((bid, bid2))
                bucket.add((bid2, bid))
        self.ids.add(bid)

    def remove_pairs(self, bid):
        """Removes every pair with given box ID. Removing is based on management type."""
        self.ids.discard(bid)
        if self.mngmt_type == MNGMT_TYPE.matrix:
            for bid2 in self.ids:
                self.pairs[bid][bid2] = False
                self.pairs[bid2][bid] = False
        else:
            for bid2 in self.ids:
                key = hash_bids(self.count, bid, bid2)
                if key in self.pairs:
                    bucket = self.pairs.get(key, set())
                    bucket.discard((bid, bid2))
                    bucket.discard((bid2, bid))
                    if len(bucket) == 0:
                        del self.pairs[key]


class GridManager:
    """Represents grid in dense matrix. Grid is containing Cell objects which manage adding and removing of pairs.
    GridManager computes size of grid based on count of objects in scene.
    Implements methods for adding, removing and updating of boxes in the scene.
    """

    def __init__(self, mngmt_type, obj_count, x_size, y_size, cell_size):
        """Computes grid size, creates and stores grid. Stores also size of a cell."""
        self.boxes = dict()
        # TODO change cell_size with the count of objects
        x_cells = int((x_size / cell_size) + 0.5)
        y_cells = int((y_size / cell_size) + 0.5)
        self.cell_size = cell_size
        # grid is represented as matrix
        self.grid = [[Cell(mngmt_type, obj_count) for y in range(y_cells)] for x in range(x_cells)]

    def add_box(self, box):
        """Creates AABB from the shape coordinates. Then marks shape id to corresponding cells."""
        # store new box in dictionary
        self.boxes[box.bid] = box
        min_cell_x, min_cell_y, max_cell_x, max_cell_y = self.__create_aabb(box.coordinates)

        # add pairs to cells under AABB of object
        for i in range(min_cell_x, max_cell_x + 1):
            for j in range(min_cell_y, max_cell_y + 1):
                self.grid[i][j].add_pairs(box.bid)

    def remove_box(self, box):
        """Removes pairs with current box id from grid."""
        min_cell_x, min_cell_y, max_cell_x, max_cell_y = self.__create_aabb(box.coordinates)

        for i in range(min_cell_x, max_cell_x + 1):
            for j in range(min_cell_y, max_cell_y + 1):
                self.grid[i][j].remove_pairs(box.bid)

        # remove box from dictionary
        try:
            del self.boxes[box.bid]
        except KeyError:
            print("ERROR: Box with id {} should be in dictionary.".format(box.bid))

    def update_boxes(self):
        """Performs movement of box and updates grid. TODO: make it effective!"""
        for _, box in self.boxes.iteritems():
            self.remove_box(box)
            # TODO must move box here!!!
            self.add_box(box)

    def __create_aabb(self, coordinates):
        """Finds left down corner and right upper corner of AABB box of object.  """
        min_x, min_y, max_x, max_y = self.__find_min_max_coordinates(coordinates)
        # get left down corner cell
        min_cell_x, min_cell_y = self.__cell(min_x, min_y)
        # get right upper corner cell
        max_cell_x, max_cell_y = self.__cell(max_x, max_y)

        return min_cell_x, min_cell_y, max_cell_x, max_cell_y

    @staticmethod
    def __find_min_max_coordinates(coordinates):
        """Gets object world coordinates.
        Returns min x, min y, max x and max y coordinates of AABB.
        """
        min_x, min_y, max_x, max_y = sys.maxint, sys.maxint, 0, 0
        for pair in coordinates:
            if pair[0] < min_x:
                min_x = pair[0]
            if pair[0] > max_x:
                max_x = pair[0]
            if pair[1] < min_y:
                min_y = pair[1]
            if pair[1] > max_y:
                max_y = pair[1]

        return min_x, min_y, max_x, max_y

    def __cell(self, x, y):
        """Returns coordinates of cell based on x and y coordinates."""
        x = int(x / self.cell_size)
        y = int(y / self.cell_size)
        return x, y

if __name__ == "__main__":
    pass
