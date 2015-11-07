"""Contains various helper functions for other modules."""
import random
from box import Box


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

if __name__ == "__main__":
    pass
