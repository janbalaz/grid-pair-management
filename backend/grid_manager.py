import math
from box import Box
from utils import MNGMT_TYPE


class Cell:
    """This class represents single cell in grid (dense matrix).
    It implements methods for adding and removing pairs.
    """

    def __init__(self, mngmt_type, obj_count=0):
        """Based on management type creates dense matrix (as lists in list in Python)
        or set of pairs. There is no need for special hashing, sets in Python use hashing as default.
        TODO: describe what is object count
        """
        self.mngmt_type = mngmt_type
        self.count = obj_count
        self.ids = set()

        if self.mngmt_type == MNGMT_TYPE.matrix:
            self.pairs = [[False for y in range(self.count)] for x in range(self.count)]
        else:
            self.pairs = set()

    def add_pairs(self, bid):
        """Adds new pairs with new object with box ID. Addition is based on management type."""
        if self.mngmt_type == MNGMT_TYPE.matrix:
            for bid2 in self.ids:
                self.pairs[bid][bid2] = True
                self.pairs[bid2][bid] = True
        else:
            for bid2 in self.ids:
                self.pairs.add((bid, bid2))
                self.pairs.add((bid2, bid))
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
                self.pairs.discard((bid, bid2))
                self.pairs.discard((bid2, bid))


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
        # get left down corner cell
        min_cell_x, min_cell_y = self.__cell(box.min_x, box.min_y)
        # get right upper corner cell
        max_cell_x, max_cell_y = self.__cell(box.max_x, box.max_y)

        # add pairs to cells under AABB of object
        for i in range(min_cell_x, max_cell_x + 1):
            for j in range(min_cell_y, max_cell_y + 1):
                self.grid[i][j].add_pairs(box.bid)

    def remove_box(self, box):
        """Removes pairs with current box id from grid."""
        # get left down corner cell
        min_cell_x, min_cell_y = self.__cell(box.min_x, box.min_y)
        # get right upper corner cell
        max_cell_x, max_cell_y = self.__cell(box.max_x, box.max_y)

        for i in range(min_cell_x, max_cell_x + 1):
            for j in range(min_cell_y, max_cell_y + 1):
                self.grid[i][j].remove_pairs(box.bid)

        # remove box from dictionary
        try:
            del self.boxes[box.bid]
        except KeyError:
            print("ERROR: Box with id {} should be in dictionary.".format(box.bid))

    def update_boxes(self):
        """Performs movement of box and updates grid."""
        for _, box in self.boxes.iteritems():
            self.remove_box(box)
            # TODO must move box here!!!
            self.add_box(box)

    def __cell(self, x, y):
        """Returns coordinates of cell based on x and y coordinates."""
        x = int(x / self.cell_size)
        y = int(y / self.cell_size)
        return x, y

if __name__ == "__main__":
    pass
