import pygame
import math
from PointVectorSector import *


# Check if Line AB and CD intersect, however will return false if the points intersect.
# This is used for checking if Created Vectors in a sector intersect
def VectorIntersectLinesNotPoints(A, B, C, D):
    Denom = (B-A)^(D-C)
    if Denom == 0:
        return False
    else:
        VectorU = ((C^(D-C))-(A^(D-C)))/Denom
        VectorV = ((A^(B-A))-(C^(B-A)))/-Denom
        if (0 < VectorU < 1) and (0 < VectorV < 1):
            return True
        else:
            return False
# Check if Line AB and CD intersect
# Used in the Actual Raycasting to check how far points are away
def VectorIntersectLinesAndPoints(A, B, C, D):
    Denom = (B-A)^(D-C)
    if Denom == 0:
        return False
    else:
        VectorU = ((C^(D-C))-(A^(D-C)))/Denom
        VectorV = ((A^(B-A))-(C^(B-A)))/-Denom
        if (0 <= VectorU <= 1) and (0 <= VectorV <= 1):
            return True
        else:
            return False

# Checks if the Triangle created by Point1, Point2 and Point3 Intersect
# NOTE: Don't know if this works or not as haven't tried it but in principle it should
# Might have to rename function IsTriangleAntiClockwise
def IsTriangleClockwise(Point1, Point2, Point3):
    return (Point2-Point1)^(Point3-Point1) > 0

# Check if Point4 is in Triangle bounded by Point1, Point2, Point3
# Used to check if a point is in a given sector
def IsPointInTriangle(Point1, Point2, Point3, Point4):
    Orientation1 = (Point2 - Point1)^(Point4 - Point1)
    Orientation2 = (Point3 - Point2)^(Point4 - Point2)
    Orientation3 = (Point1 - Point3)^(Point4 - Point3)
    return ((Point2-Point1)^(Point3-Point1) > 0) and (Orientation1 > 0 and Orientation2 > 0 and Orientation3 > 0)

def IsPointInRectangle(Point1, Point2, Point3, Point4, Point5):
    PointMax = Point(max(Point1.x, Point2.x, Point3.x, Point4.x), max(Point1.y, Point2.y, Point3.y, Point4.y))
    PointMin = Point(min(Point1.x, Point2.x, Point3.x, Point4.x), min(Point1.y, Point2.y, Point3.y, Point4.y))
    return (PointMin <= Point5 <= PointMax)

# Map Class deals with all the Map creation Functions
class Map():
    # Initialise Map with WorldSize a list of [width, height]
    def __init__(self, WorldSize):
        self.WorldSize = WorldSize
        self.Sector = 0
        self.Sectors = {0: Sector(Point(0, 0), Point(9,0), Point(0,9), Point(9, 9))}


        self.UserVectors = {}

        self.ComputerVectors = {}
        self.Vectors = {}

    # Check if a point is still inside a sector and if it is not find out where it is
    def StillInSector(self, RelativeMousePoint):
        if IsPointInTriangle(*self.Sectors[Sector], RelativeMousePoint) == False:
            for key, value in self.Sectors:
                pass
            # TODO: REASSIGN SECTOR if value is in key

    def NewVector(self, NewVector):
        # ProposedVectorsDict is all the possible combinations of Vectors from the point to the Sector Points
        ProposedVectorsDict = {}
        for VectorPointIndex in range(len(NewVector)):
            # Create New Vectors going from the point to all points in Sector
            ProposedVectorsFromPoint = dict(enumerate(map(lambda SectorPoint: Vector(NewVector[VectorPointIndex], SectorPoint), self.Sectors[self.Sector]), start=len(ProposedVectorsDict)))
            ProposedVectorsDict = {**ProposedVectorsDict, **ProposedVectorsFromPoint}

        # Remove any intersecting Vectors
        for BlackKey in list(ProposedVectorsDict.keys()):
            # Create a list of ProposedVectorsDict that does not include BlackKey.
            # This means we will not Intersect BlackKey with itself and try and delete it
            blacklistdict = [WhiteValue for WhiteKey, WhiteValue in ProposedVectorsDict.items() if WhiteKey != BlackKey]
            Intersection = list(filter(lambda ProposedPoint: VectorIntersectLinesNotPoints(*ProposedVectorsDict[BlackKey], *ProposedPoint), blacklistdict))
            if len(Intersection) > 0:
                del ProposedVectorsDict[BlackKey]

        # Add NewVector to UserVectors and to Vectors
        self.UserVectors[len(self.UserVectors)] = NewVector
        self.Vectors[(0, len(self.UserVectors))]= NewVector
        # Reindex ProposedVectorsDict and add to ComputerVectors
        ProposedVectorsDict = dict(enumerate(ProposedVectorsDict.values(), start=len(self.ComputerVectors)))
        self.ComputerVectors.update(ProposedVectorsDict)
        self.Vectors.update(dict(((1, Key), Value) for Key, Value in ProposedVectorsDict.items()))
        #Return a dict of all new vectors created so we can blit them to Pygame LineSurface

        return [NewVector] + list(ProposedVectorsDict.values())
