import math

# Point is a list of [x, y]
class Point(list):
    def __init__(self, *args):
        """List object [x, y]"""
        super(Point, self).__init__(args)

    def __add__(self, other):
        if type(other) is self.__class__:
            return self.__class__(self[0] + other[0], self[1] + other[1])
        else:
            return self.__class__(self[0] + other, self[1] + other)

    def __sub__(self, other):
        if type(other) is self.__class__:
            return self.__class__(self[0] - other[0], self[1] - other[1])
        else:
            return self.__class__(self[0] - other, self[1] - other)

    # Division Operator divides both coordinates by scalar or by respective coordinates if other Point
    # Shouldn't really be needed
    def __truediv__(self, other):
        if type(other) is self.__class__:
            return self.__class__(self[0] / other[0], self[1] / other[1])
        if type(other) is int or other is float:
            return self.__class__(self[0]/other, self[1]/other)

    # Vector Dot Product for Point
    # Point Multiplication if anything else
    def __mul__(self, other):
        if type(other) is self.__class__:
            return (self[0] * other[0]) + (self[1] * other[1])
        else:
            return self.__class__(self[0]*other, self[1]*other)

    # Vector Cross Product. For example Point1 ^ Point2 = Point1.x*Point2.y - Point2.x*Point1.y
    def __xor__(self, other):
        return self[0]*other[1]-self[1]*other[0]

    def __lt__(self, other):
        return self[0] < other[0] and self[1] < other[1]
    def __le__(self, other):
        return self[0] <= other[0] and self[1] <= other[1]
    def __eq__(self, other):
        return self[0] == other[0] and self[1] == other[1]
    def __ne__(self, other):
        return self[0] != other[0] and self[1] != other[1]
    def __gt__(self, other):
        return self[0] > other[0] and self[1] > other[1]
    def __ge__(self, other):
        return self[0] >= other[0] and self[1] >= other[1]
    def __hash__(self):
        return hash((self[0], self[1]))

    # Changes Point into int. Used for when drawing coordinates.
    def PointToIntPoint(self):
        return self.__class__(int(self[0]), int(self[1]))
    @property
    def length(self):
        return math.sqrt(self[0] ** 2, self[1] ** 2)
    @property
    def x(self): return self[0]
    @x.setter
    def x(self, value):
        self[0] = value

    @property
    def y(self):
        return self[1]
    @y.setter
    def y(self, value):
        self[1] = value

# Vector: A list of two points.
class Vector(list):
    """Vector: A list of two points. [point1, Point2]"""
    Color = None
    def __init__(self, *args):
        super(Vector, self).__init__(args)
    def __sub__(self, Object):
        if Object is type(Point):
            return self.__class__(self[0] - Object, self[1] - Object)
        elif Object is type(Vector):
            return self.__class__(self[0] - Object[0], self[1] - Object[1])
    def __add__(self, Object):
        if Object is type(Point):
            return self.__class__(self[0] + Object, self[1] + Object)
        elif Object is type(Vector):
            return self.__class__(self[0] + Object[0], self[1] + Object[1])
    def __hash__(self):
        return hash((self[0], self[1]))

    def Magnitude(self):
        """Get Magnitude of the Vector"""
        return math.sqrt(abs(self[0].x - self[1].x)**2 + abs(self[0].y - self[1].y)**2)
    def Direction(self):
        """Get Direction of the Vector"""
        return math.atan2(abs(self[0].y - self[1].y) / abs(self[0].x - self[1].x))
    @property
    def point1(self):
        return self[0]
    @point1.setter
    def point1(self, value):
        self[0] = value

    @property
    def point2(self):
        return self[1]
    @point2.setter
    def point2(self, value):
        self[1] = value


class Sector(list):
    """
    Sector is a List of 3 or more points
    Sector is polygon that is used to speed up ray casting.
    """
    def __init__(self, *args):
        super(Sector, self).__init__(args)
    def __hash__(self):
        return hash(tuple(self))

    def VectorsIter(self):
        Index = -0
        while Index < len(self):
            Index += 1
            yield Vector(self[Index-1], self[(Index) % len(self)])


    @property
    def Vectors(self):
        return [Vector(self[Index], self[(Index+1) % len(self)]) for Index in range(len(self))]
