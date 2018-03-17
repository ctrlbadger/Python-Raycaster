import math

class Point(list):
    def __init__(self, *args):
        super(Point, self).__init__(args)
        self._y = self[1]
        # Creates List with strings corresponding to Vectors
        self.VectorParents = []
    def __add__(self, other):
        return self.__class__(self[0] + other[0], self[1] + other[1])
    def __sub__(self, other):
        return self.__class__(self[0] - other[0], self[1] - other[1])
    def __truediv__(self, other):

        if type(other) is self.__class__:
            return self.__class__(self[0] / other[0], self[1] / other[1])
        else:
            return self.__class__(self[0]/other, self[1]/other)
    # Vector Dot Product for Point
    # Point Multiplication if anything else
    def __mul__(self, other):
        if type(other) is self.__class__:
            return self.__class__(self[0] * other[0], self[1] * other[1])
        else:
            return self.__class__(self[0]*other, self[1]*other)
    # Vector Cross Product
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
    Color = None
    def __init__(self, *args):
        super(Vector, self).__init__(args)
    def __sub__(self, Point1):
        if Point1 is type(Point):
            return self.__class__(self[0]*- Point1, self[1] - Point1)
    def __contains__(self, Point1):
        return (Point1 == self[0] or Point1 == self[1])

    def HasPoint(self, Point):
        if Point in self:
            return self.index(Point)
        else:
            return False
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
    def __init__(self, *args):
        super(Sector, self).__init__(args)

    def IsPointInSectorPointBased(self, Point):
        Sides = []
        # Dot cross the Vectors with the Point Vector
        # To see which side side they are on
        Sides.append((self[1]-self[0]) ^ (Point - Vector[0]))
        Sides.append((self[2]-self[1]) ^ (Point - Vector[1]))
        Sides.append((self[0]-self[2]) ^ (Point - Vector[2]))
        if ((self[1] - self[0]) ^ (self[2] - self[0])) > 0:
            return (len(list(filter(lambda x: x >= 0, Sides))) == 3)
        else:
            return (len(list(filter(lambda x: x <= 0, Sides))) == 3)

    def __contains__(self, Point1):
        return (Point1 == self[0] or Point1 == self[1])

    def HasPoint(self, Point):
        if Point in self:
            return self.index(Point)
        else:
            return False

    @property
    def Vectors(self):
        return [Vector(self[0], self[1]), Vector(self[1], self[2]), Vector(self[2], self[0])]
    @property
    def Point1(self): return self[0]
    @Point1.setter
    def Point1(self, value):
        self[0] = value

    @property
    def Point2(self): return self[1]
    @Point2.setter
    def Point2(self, value):
        self[1] = value

    @property
    def Point3(self): return self[2]
    @Point3.setter
    def Point3(self, value):
        self[2] = value
