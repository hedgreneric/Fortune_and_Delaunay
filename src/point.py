import math as m

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __neg__(self):
        return Point(-self.x, -self.y)
    
    def __add__ (self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    
    def __isub__(self, other):
        return Point(self.x - other.x, self.y - self.y - other.y)
    
    def __mul__(self, t):
        return Point(self.x * t, self.y * t)
    
    def __imul__(self, t):
        self.x *= t
        self.y *= t
        return self

    def __rmul__(self, t):
        return self * t

    def __str__(self):
        return f"({self.x}, {self.y})"

    def getOrthogonal(self):
        return Point(-self.y, self.x)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def getNorm(self):
        return m.sqrt(self.x * self.x + self.y * self.y)

    def getDistance(self, other):
        return (self - other).getNorm()

    def getDet(self, other):
        return self.x * other.y - self.y * other.x