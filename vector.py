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

    def __mul__(self, other):
        if isinstance(other, Vector2D):
            x = self.x * other.x
            y = self.y * other.y
        elif isinstance(other, int):
            x = self.x * other
            y = self.y * other
        else:
            raise TypeError("Unsupported operand types")
        return Vector2D(x, y)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __repr__(self):
        return ("Vector2D (x={}, y={})".format(self.x, self.y))

if __name__ == '__main__':
    print(Vector2D(4, 2) + Vector2D(2, 3))
    print(Vector2D(4, 2) - Vector2D(2, 3))
    print(Vector2D(4, 2) * 2)
    print(Vector2D(4, 2) * Vector2D(2, 2))
