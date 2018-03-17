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
        print(VectorU)
        VectorV = ((A^(B-A))-(C^(B-A)))/-Denom
        print(VectorV)
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
        print(VectorU)
        VectorV = ((A^(B-A))-(C^(B-A)))/-Denom
        print(VectorV)
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



# Map Class deals with all the Map creation Functions
class Map():
    # Initialise Map with WorldSize a list of [width, height]
    def __init__(self, WorldSize):
        self.WorldSize = WorldSize
        self.Sector = 0
        self.Sectors = {0: Sector(Point(0,0), Point(9, 0), Point(0, 9)), 1: Sector(Point(9, 0), Point(0, 9), Point(9, 9))}

        self.UserVectorCount = 0
        self.UserVectors = SubVectorDecorator(self)
        self.UserVectors.VectorIndex = 0
        self.ComputerVectorCount = 0
        self.ComputerVectors = SubVectorDecorator(self)
        self.ComputerVectors.VectorIndex = 1
        self.Vectors = {}
    def StillInSector(self, RelativeMousePoint):
        if IsPointInTriangle(*self.Sectors[Sector], RelativeMousePoint) == False:
            for key, value in self.Sectors:
                pass
            # TODO: REASSIGN SECTOR if value is in key

    def NewVector(self, NewVector):
        self.ComputerVectors
        self.UserVectors
        self.UserVectors[self.UserVectorCount] = NewVector

        ProposedVectorCount = self.ComputerVectorCount
        ProposedVectorsDict = {}
        ProposedVectorsDict.update(self.ComputerVectors)

        # Create new vectors to point
        for VectorPointIndex in range(len(NewVector)):
            # Create all proposed vectors for sector
            ProposedVectorsList = list(map(lambda SectorPoint: Vector(NewVector[VectorPointIndex], SectorPoint), self.Sectors[self.Sector]))
            VectorDict = dict(enumerate(ProposedVectorsList, start=ProposedVectorCount))
            print("Values in VectorDict at creation", VectorDict)
            for key in list(VectorDict.keys()):
                # First check the Sectors and see if there is any intersections
                Intersection = list(filter(lambda SectorVector: VectorIntersectLinesNotPoints(*SectorVector, *VectorDict[key]), self.UserVectors.values()))
                if len(Intersection) > 0:
                    del VectorDict[key]
            print("Values in VectorDict at sector intersection", VectorDict)
            for key in list(VectorDict.keys()):
                # First check the Sectors and see if there is any intersections
                Intersection = list(filter(lambda SectorVector: VectorIntersectLinesNotPoints(*SectorVector, *VectorDict[key]), self.Sectors[self.Sector].Vectors))
                if len(Intersection) > 0:
                    del VectorDict[key]
            print("Values in VectorDict at sector intersection", VectorDict)
            # So we've now checked if there are any conflicts with Sectors now to check for conflicts with any new Vectors we have created
            VectorDict.update(ProposedVectorsDict)

            for BlackKey in list(VectorDict.keys()):
                blacklistdict = [WhiteValue for WhiteKey, WhiteValue in VectorDict.items() if WhiteKey != BlackKey]
                print("With key", BlackKey, "we get the following dict", blacklistdict)
                Intersection = list(filter(lambda ProposedPoint: VectorIntersectLinesNotPoints(*VectorDict[BlackKey], *ProposedPoint), blacklistdict))

                if len(Intersection) > 0:
                    del VectorDict[BlackKey]

            ProposedVectorCount += len(VectorDict)
            print("Proposed Values in VectorDict at end of for loop", VectorDict)
            ProposedVectorsDict = {**ProposedVectorsDict, **VectorDict}
            print("ProposedVectorsDict at end of for loop", ProposedVectorsDict)
        self.ComputerVectorCount += len(VectorDict)
        ProposedVectorsDict = dict(enumerate(ProposedVectorsDict.values(), start=ProposedVectorCount))
        print("Our proposed Vectors are: ", ProposedVectorsDict)
        self.ComputerVectors.update(ProposedVectorsDict)

        self.UserVectorCount += 1
        #Return a dict of all new vectors created so we can blit them to Pygame LineSurface
        return [NewVector] + list(ProposedVectorsDict.values())
    # @property
    # def UserVectors(self): return self._UserVectors
    # @UserVectors.setter # TODO WORK OUT HOW TO DO THIS WITH DICTS
    # def UserVectors(self, key, value):
    #     self._UserVectors[key] = value
    #     self._Vectors['UserVectors'][key] = value
    #
    # @property
    # def ComputerVectors(self): return self._ComputerVectors
    # @ComputerVectors.setter # TODO WORK OUT HOW TO DO THIS WITH DICTS
    # def ComputerVectors(self, key, value):
    #     self._ComputerVectors[key] = value
    #     self._Vectors['ComputerVectors'][key] = value
    #
    # @property
    # def Vectors(self):
    #     return self._Vectors

class  SubVectorDecorator(dict):
    def __init__(self, parent):
        self.LastParent = [parent]
    def __getitem__(self, key):
        return dict.__getitem__(self, key)
    def __setitem__(self, key, value):
        print("WE'VE BEEN CALLED")
        self.LastParent[0].Vectors[(self.VectorIndex, key)] = value
        dict.__setitem__(self, key, value)
    def __delitem__(self, key):
        del self.LastParent[(self.VectorIndex, key)]
        dict.__delitem__(self, key)
    """def update(self, *args):
        self.LastParent.Vectors
        dict.__update__(self, args)
    """
