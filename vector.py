import math

class Vector2D:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector2D(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vector2D(x, y)

    def __rmul__(self, other):
        if isinstance(other, Vector2D):
            x = self.x * other.x
            y = self.y * other.y
        else isinstance(other, int):
            x = self.x * other
            y = self.y * other
        return Vector2D(x, y)

    def __repr__(self):
        return ("Vector2D (x={}, y={})".format(self.x, self.y))


print(Vector2D(4, 2) + Vector2D(2, 3))
