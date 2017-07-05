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
            return self.x * other.x + self.y * other.y

        elif isinstance(other, int) or isinstance(other, float):
            x = self.x * other
            y = self.y * other
            return Vector2D(x, y)
        else:
            raise TypeError("Unsupported operand types")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __repr__(self):
        return ("Vector2D(x={:.2f}, y={:.2f})".format(self.x, self.y))

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def angle(self, other):
        return math.acos(self.__mul__(other) 
                         / (self.__abs__() * other.__abs__()))

    def rotate(self, angle):
        x = self.x * math.cos(angle) - self.y * math.sin(angle)
        y = self.x * math.sin(angle) + self.y * math.cos(angle)
        return Vector2D(x, y)
        
    def is_perpendicular(self, other):
        return self.__mul__(other) == 0


if __name__ == '__main__':
    A = Vector2D(4, 2)
    print(A + Vector2D(2, 3))
    print(A - Vector2D(2, 3))
    print(A * 2.55)
    print(A * Vector2D(5, 2))
    print(abs(A))
    print(Vector2D(1, 6).angle(A))
    print(Vector2D(0, 5).is_perpendicular(Vector2D(5, 0)))
    print(Vector2D(0, 5).rotate(-math.pi))
