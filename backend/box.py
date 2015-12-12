import sys


class Box:
    """Defines object with real world coordinates within AABB box.  """

    def __init__(self, bid, coordinates):
        self.bid = bid
        self.coordinates = coordinates
        # TODO add generated random velocity
        self.min_x, self.min_y = sys.maxsize, sys.maxsize
        self.max_x, self.max_y = -sys.maxsize, -sys.maxsize
        self.__create_aabb()

    def __create_aabb(self):
        """Gets object world coordinates.
        Stores min x, min y, max x and max y coordinates of AABB.
        """
        self.min_x, self.min_y = map(min, zip(*self.coordinates))
        self.max_x, self.max_y = map(max, zip(*self.coordinates))

    def move_box(self):
        # TODO add movement
        pass
