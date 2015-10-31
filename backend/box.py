import sys


class Box:

    def __init__(self, coordinates):
        self.bid = id(self)
        # TODO generate random velocity
        self.min_x, self.min_y, self.max_x, self.max_y = sys.maxint, sys.maxint, 0, 0
        self.__create_aabb(coordinates)

    def __create_aabb(self, coordinates):
        """Gets object world coordinates.
        Returns min x, min y, max x and max y coordinates of AABB.
        """
        for pair in coordinates:
            if pair[0] < self.min_x:
                self.min_x = pair[0]
            if pair[0] > self.max_x:
                self.max_x = pair[0]
            if pair[1] < self.min_y:
                self.min_y = pair[1]
            if pair[1] > self.max_y:
                self.max_y = pair[1]

    def move_box(self):
        # TODO
        pass
