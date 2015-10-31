import math
from box import Box


class Cell:
    ids = set()
    pairs = set()

    def __str__(self):
        return str(self.pairs)


class GridManager:

    def __init__(self, x_size, y_size, cell_size):
        """Computes grid size, creates and stores grid. Stores also size of a cell."""
        # TODO change cell_size with the count of objects
        x_cells = int((x_size / cell_size) + 0.5)
        y_cells = int((y_size / cell_size) + 0.5)
        self.cell_size = cell_size
        # grid is represented as matrix
        self.grid = [[Cell() for y in range(y_cells)] for x in range(x_cells)]
        print(self.grid)

    def add_box(self, box):
        """Creates AABB from the shape coordinates. Then marks shape id to corresponding cells."""
        # get left down corner cell
        min_cell_x, min_cell_y = self.__cell(box.min_x, box.min_y)
        # get right upper corner cell
        max_cell_x, max_cell_y = self.__cell(box.max_x, box.max_y)

        for i in range(min_cell_x, max_cell_x + 1):
            for j in range(min_cell_y, max_cell_y + 1):
                cell = self.grid[i][j]
                # pair current object with other objects in cell
                for oid in cell.ids:
                    cell.pairs.add((oid, box.id))
                    cell.pairs.add((box.id, oid))
                cell.ids.add(box.id)

    def remove_box(self, box):
        """"""
        # get left down corner cell
        min_cell_x, min_cell_y = self.__cell(box.min_x, box.min_y)
        # get right upper corner cell
        max_cell_x, max_cell_y = self.__cell(box.max_x, box.max_y)

        for i in range(min_cell_x, max_cell_x + 1):
            for j in range(min_cell_y, max_cell_y + 1):
                cell = self.grid[i][j]
                # at first remove box id from cell
                cell.ids.discard(box.id)
                # pair current object with other objects in cell and try to remove them
                for oid in cell.ids:
                    cell.pairs.discard((oid, box.id))
                    cell.pairs.discard((box.id, oid))

    def update_box(self, box):
        self.remove_box(box)
        # TODO must move box here!!!
        self.add_box(box)

    def __cell(self, x, y):
        """Returns coordinates of cell from x and y coordinates."""
        x = int(x / self.cell_size)
        y = int(y / self.cell_size)
        return x, y

if __name__ == "__main__":
    gm = GridManager(100, 60, 20)
