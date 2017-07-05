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

    def __mul__(self, scalar):
        x = self.x * scalar
        y = self.y * scalar
        return Vector2D(x, y)
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, scalar):
        x = self.x / scalar
        y = self.y / scalar
        return Vector2D(x, y)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __repr__(self):
        return ("Vector2D(x={:.2f}, y={:.2f})".format(self.x, self.y))

    def angle(self, other):
        return math.acos(self.dot(other) 
                         / (self.__abs__() * other.__abs__()))

    def rotate(self, angle):
        x = self.x * math.cos(angle) - self.y * math.sin(angle)
        y = self.x * math.sin(angle) + self.y * math.cos(angle)
        return Vector2D(x, y)
        
    def is_perpendicular(self, other):
        return self.__mul__(other) == 0
    @property
    def x(self):
        return self.x

    @property
    def y(self):
        return self.y

    @property
    def data(self):
        return (self.x, self.y)
