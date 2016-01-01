import sys


class Box:
    """Defines object with real world coordinates within AABB box.  """

    def __init__(self, bid, coordinates, dx, dy):
        self.bid = bid
        self.dx = dx
        self.dy = dy
        self.coordinates = coordinates
        self.min_x = self.min_y = sys.maxsize
        self.max_x = self.max_y = -sys.maxsize
        self.__create_aabb()

    def __create_aabb(self):
        """Gets object world coordinates.
        Stores min x, min y, max x and max y coordinates of AABB.
        """
        self.min_x, self.min_y = map(min, zip(*self.coordinates))
        self.max_x, self.max_y = map(max, zip(*self.coordinates))

    def move_box(self, x_size, y_size):
        """"Movement of object and controll if borders are not crossed. Stands still if borders should be crossed
        until next movement.
        """
        coordinates = []
        changed_dt = False
        for (x, y) in self.coordinates:
            tx = x + self.dx
            ty = y + self.dy
            if tx <= 0 or tx >= x_size:
                changed_dt = True
                self.dx = -self.dx
            if ty <= 0 or ty >= y_size:
                changed_dt = True
                self.dy = -self.dy
            coordinates.append((tx, ty))
        if not changed_dt:
            self.coordinates = coordinates
        self.__create_aabb()

