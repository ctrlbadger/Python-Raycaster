from PointVectorSector import *


# Check if Line AB and CD intersect, however will return false if the points intersect.
# This is used for checking if Created Vectors in a sector intersect
# https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect/565282#565282

# I actually think this is the Dot Cross Product
def Projection(A, B):
    return (A.x * B.x) + (A.y*B.y)


def VectorIntersectLinesNotPoints(P, Ps, Q, Qs):
    R = (Ps-P)
    S = (Qs-Q)
    # Collinear
    if R ^ S == 0 and (Q-P) ^ R == 0:
        try:
            # Check if both vectors each other
            t_zero = Projection((Q-P), R) / Projection(R, R)
            t_one = Projection((Q+S-P), R) / Projection(R, R)
            return (0 < t_zero < 1) or (0 < t_one < 1)
        except ZeroDivisionError:
            return True
    # Parallel but not collinear
    elif R ^ S == 0 and (Q-P) ^ R != 0:
        return False
    else:
        t = ((Q-P) ^ S)/(R ^ S)
        u = ((Q-P) ^ R)/(R ^ S)
        return (0 < t < 1) and (0 < u < 1)

# Check if Line AB and CD intersect
# Used in the Actual Raycasting to check how far points are away
def VectorIntersectLinesAndPoints(A, B, C, D):
    Denom = (B-A)^(D-C)
    if Denom == 0:
        if (C-A) <= (B-A) or (D-A) <= (B-A):
            return True
        else:
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
    return ((Point2-Point1)^(Point3-Point1) < 0) and (Orientation1 < 0 and Orientation2 < 0 and Orientation3 < 0)


# Checks if a Point is in a Sector, also checks the lines bounded by the Sector
def IsPointInSectorAndPoints(Sector1, CheckPoint):
    Orientations = [((Sector1[Index] - Sector1[(Index - 1) % len(Sector1)]) ^ (CheckPoint - Sector1[(Index - 1) % len(Sector1)])) for Index in range(len(Sector1))]
    if (((Sector1[1]-Sector1[0])^(Sector1[2]-Sector1[0])) < 0):
        return len(list(filter(lambda Orientation: Orientation > 0, Orientations))) == 0
    else:
        return len(list(filter(lambda Orientation: Orientation < 0, Orientations))) == 0


# Checks if a point is inside a sector, does not check lines of sector
def IsPointInSectorNotPoints(Sector1, CheckPoint):
    Orientations = [((Sector1[Index] - Sector1[(Index - 1) % len(Sector1)]) ^ (CheckPoint - Sector1[(Index - 1) % len(Sector1)])) for Index in range(len(Sector1))]
    if (((Sector1[1]-Sector1[0])^(Sector1[2]-Sector1[0])) < 0):
        return len(list(filter(lambda Orientation: Orientation >= 0, Orientations))) == 0
    else:
        return len(list(filter(lambda Orientation: Orientation <= 0, Orientations))) == 0


# Map Class deals with all the Map creation Functions
class Map():
    # Initialise Map with WorldSize a list of [width, height]
    def __init__(self, WorldSize):
        self.WorldSize = WorldSize
        self.Sector = 0
        self.Sectors = {}
        self.Vectors = {}
        self.UserVectors = {}
        self.ComputerVectors = {}

        # Just going to hard code in the First sector might channge it later
        self.Sectors = {0: Sector(Point(0, 0), Point(9,0), Point(9, 9), Point(0,9))}
        self.PointTable = {Point(0, 0): [0], Point(9,0): [0], Point(0,9): [0], Point(9, 9): [0]}
        self.ComputerVectors = dict(enumerate(self.Sectors[self.Sector].Vectors))
        self.Vectors.update(dict(((1, Key), Value) for Key, Value in self.ComputerVectors.items()))

    # Try and locate a point, will search any sectors around it and then every sector. Yes I know it's not that efficient
    def FindNewSector(self, CheckSector, CheckPoint):
        # Find all adjacent sectors
        AdjacentSectors = [self.PointTable[CheckSectorPoint] for CheckSectorPoint in self.Sectors[CheckSector]]
        print(AdjacentSectors)
        # NewSet =  set([item for sublist in AdjacentSectorsIndex for item in sublist]) - set(CheckSector)
        NewSet = set([item for items in AdjacentSectors for item in items]) - set(CheckPoint)

        # Check if point is in Adjacent sectors
        for PossibleSector in list(NewSet):
            print("PossibleSector", PossibleSector)
            if IsPointInSectorAndPoints(self.Sectors[PossibleSector], CheckPoint): return PossibleSector

        #Huh that's odd guess we are going to have to go on a goose chase to find this one
        for PossibleSector in self.Sectors.keys():
            if IsPointInSectorAndPoints(self.Sectors[PossibleSector], CheckPoint): return PossibleSector
        #Might be out of range so best to leave it alone
        return CheckSector

    def NewVector(self, NewVector):

        if not IsPointInSectorAndPoints(self.Sectors[self.Sector], NewVector[0]):
            self.Sector = self.FindNewSector(self.Sector, NewVector[0])
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
            blacklistdict.append(NewVector)

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
        self.CalculateSectors(NewVector, ProposedVectorsDict)
        return [NewVector] + list(ProposedVectorsDict.values())

    # Create new Sectors from new vector and the proposed computer vectors created from it
    def CalculateSectors(self, NewVector, ProposedVectorsDict):
        ProposedVectorSets = list(map(lambda ProposedVectors: set(ProposedVectors), list(ProposedVectorsDict.values())))
        FoundSectors = []

        # Find Sectors bounded by a sector wall and a point in the NewVector
        for NewPoint in NewVector:
            Intersection = list(filter(lambda VectorPoint: ((set((VectorPoint[0], NewPoint)) in ProposedVectorSets) and (set((VectorPoint[1], NewPoint)) in ProposedVectorSets)), self.Sectors[self.Sector].Vectors))
            for Index in Intersection:
                NewSector = set((*self.Sectors[self.Sector].Vectors[self.Sectors[self.Sector].Vectors.index(Index)], NewPoint))
                if NewSector not in FoundSectors:
                    FoundSectors.append(NewSector)
        
        # Find Sectors bounded by NewVector and a sector point
        for SectorPoint in self.Sectors[self.Sector]:
            if (set((SectorPoint, NewVector[0])) in ProposedVectorSets) and (set((SectorPoint, NewVector[1])) in ProposedVectorSets):
                NewSector = set((*NewVector, SectorPoint))
                if NewSector not in FoundSectors:
                    FoundSectors.append(NewSector)

        # Remove any sectors that have NewVector Points in them as this would overlap
        PointInSector = list(filter(lambda NewSector: IsPointInSectorNotPoints(Sector(*NewSector), NewVector[0]) or IsPointInSectorNotPoints(Sector(*NewSector), NewVector[1]), FoundSectors))
        for Index in PointInSector:
            del FoundSectors[FoundSectors.index(Index)]
        FoundSectors = list(map(lambda FoundSector: Sector(*FoundSector), FoundSectors))
        FoundDict = dict(enumerate(FoundSectors, start=len(self.Sectors)))

        
        # Now to remove current sector from the PointTable and remove it from dict of Sectors
        for OldSectorPoint in self.Sectors[self.Sector]:
            self.PointTable[OldSectorPoint].remove(self.Sector)
        del self.Sectors[self.Sector]

        for SectorKey, FoundSector in FoundDict.items():
            for SectorPoint in FoundSector:
                if SectorPoint in self.PointTable:
                    self.PointTable[SectorPoint].append(SectorKey)
                else:
                    self.PointTable[SectorPoint] = [SectorKey]



        self.Sectors.update(FoundDict)
        self.Sector += 1
        return FoundSectors
