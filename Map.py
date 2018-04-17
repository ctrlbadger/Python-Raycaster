from PointVectorSector import *
import pygame


def VectorIntersectLinesNotPoints(P, Ps, Q, Qs):
    """
    Check if Line P, Ps and Q, Qs intersect, however will return false if the points intersect.
    This is used for checking if Created Vectors in a sector intersect
    https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect/565282#565282
    """
    R = (Ps-P)
    S = (Qs-Q)
    # Collinear
    if R ^ S == 0 and (Q-P) ^ R == 0:
        try:
            # Check if both vectors each other
            t_zero = ((Q - P) * R) / (R * R)
            t_one = ((Q + S - P) * R) / (R * R)
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


def VectorIntersectLinesAndPoints(P, Ps, Q, Qs):
    """Check if Line P, Ps and Q, Qs intersect"""
    R = (Ps-P)
    S = (Qs-Q)
    # Collinear
    if R ^ S == 0 and (Q-P) ^ R == 0:
        try:
            # Check if both vectors each other
            t_zero = ((Q - P) * R) / (R * R)
            t_one = ((Q + S - P) * R) / (R * R)
            return (0 <= t_zero <= 1) or (0 <= t_one <= 1)
        except ZeroDivisionError:
            
            return True
    # Parallel but not collinear
    elif R ^ S == 0 and (Q-P) ^ R != 0:
        return False
    else:
        t = ((Q-P) ^ S)/(R ^ S)
        u = ((Q-P) ^ R)/(R ^ S)
        return (0 <= t <= 1) and (0 <= u <= 1)



# Checks if the Triangle created by Point1, Point2 and Point3 Intersect
# NOTE: Don't know if this works or not as haven't tried it but in principle it should
# Might have to rename function IsTriangleAntiClockwise
def IsTriangleClockwise(Point1, Point2, Point3):
    return (Point2-Point1)^(Point3-Point1) >= 0

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
        self.DeletedUserVectors = 0

        self.ComputerVectors = {}
        self.DeletedComputerVectors = 0

        # Just going to hard code in the First sector might channge it later
        self.Sectors = {0: Sector(Point(0, 0), Point(9,0), Point(9, 9), Point(0,9))}
        self.DeletedSectors = 0
        self.RemovedVectors = []

        self.PointTable = {Point(0, 0): [0], Point(9,0): [0], Point(0,9): [0], Point(9, 9): [0]}
        self.ComputerVectors = dict(enumerate(self.Sectors[self.Sector].Vectors))
        
        self.Vectors.update(dict(((1, Key), Value) for Key, Value in self.ComputerVectors.items()))

    # Try and locate a point, will search any sectors around it and then every sector. Yes I know it's not that efficient
    def FindNewSector(self, CheckSector, CheckPoint):
        # Find all adjacent sectors
        AdjacentSectors = [self.PointTable[CheckSectorPoint] for CheckSectorPoint in self.Sectors[CheckSector]]
        # NewSet =  set([item for sublist in AdjacentSectorsIndex for item in sublist]) - set(CheckSector)
        NewSet = set([item for items in AdjacentSectors for item in items]) - set(CheckPoint)

        # Check if point is in Adjacent sectors
        for PossibleSector in list(NewSet):
            if IsPointInSectorAndPoints(self.Sectors[PossibleSector], CheckPoint): return PossibleSector

        #Huh that's odd guess we are going to have to go on a goose chase to find this one
        for PossibleSector in self.Sectors.keys():
            if IsPointInSectorAndPoints(self.Sectors[PossibleSector], CheckPoint): return PossibleSector
        #Might be out of range so best to leave it alone
        return CheckSector

    def SolveNewVectorSectors(self, NewVector):
        NewVectorSectorIntersects = []
        for NewPoint in NewVector:
            SectorPointDict = set([SectorKey for SectorKey, SectorValue in self.Sectors.items() if IsPointInSectorAndPoints(SectorValue, NewPoint)])
            NewVectorSectorIntersects.append(SectorPointDict)
        if len(NewVectorSectorIntersects[0]&NewVectorSectorIntersects[1]) == 1:
            self.Sector = [*(NewVectorSectorIntersects[0] & NewVectorSectorIntersects[1])][0]
            
        # elif len(NewVectorSectorIntersects[0]&NewVectorSectorIntersects[1]) > 1:
            # So I think this is the case where we have a vector on a new line
            # TODO: Figure out what the hell to do
        
        else:
            # Get set of ComputerVectors that intersect with NewVector and find all corresponding Sectors 
            IntersectedVectors = {VectorKey:frozenset(IntersectedVector) for VectorKey, IntersectedVector in self.ComputerVectors.items() if VectorIntersectLinesNotPoints(*IntersectedVector, *NewVector)}
            IntersectedVectors = {VectorKey:VectorValue for VectorKey, VectorValue in IntersectedVectors.items() if len(list(filter(lambda CheckingVector: VectorIntersectLinesNotPoints(*CheckingVector, *VectorValue), IntersectedVectors.values()))) == 0}
            IntersectedSectors = {SectorKey:SectorValue for SectorKey, SectorValue in self.Sectors.items() if bool(len(set(IntersectedVectors.values()) & set(map(frozenset, SectorValue.Vectors))))}
            NewSectorVectors = set()
            for CurrentSector in list(IntersectedSectors.values()):
                NewVectors = set([frozenset(CurrentVector) for CurrentVector in CurrentSector.Vectors]) - set(IntersectedVectors.values())
                NewSectorVectors.update(frozenset(NewVectors))
            
            SelectedVector = [*NewSectorVectors.pop()]
            NewSectorPoints = [SelectedVector[1]]
            SectorVectorSetLength = len(NewSectorVectors)
            for _ in range(SectorVectorSetLength):
                FoundVector = list(filter(lambda CurrentVector: SelectedVector[1] in CurrentVector, NewSectorVectors))
                FoundVector = [*FoundVector[0]]

                # Reorder the new Vector and append the new point to Points
                Index = FoundVector.index(SelectedVector[1])
                NewSectorPoints.append(FoundVector[(Index + 1) % 2])
                SelectedVector = [FoundVector[Index], FoundVector[(Index + 1) % 2]]
                NewSectorVectors.remove(frozenset(FoundVector))
                
            # Remove Sectors from Point Table. Remove IntersectedVectors from ComputerVectors. Remove IntersectedSectors from Sector
            for IntersectedVectorKey in IntersectedVectors.keys():
                self.RemovedVectors.append(self.ComputerVectors[IntersectedVectorKey])
                del self.ComputerVectors[IntersectedVectorKey]
                self.DeletedComputerVectors += 1
                del self.Vectors[(1, IntersectedVectorKey)]
                

            for IntersectedSectorsKey, IntersectedSector in IntersectedSectors.items():
                for IntersectedPoint in IntersectedSector:
                    self.PointTable[IntersectedPoint].remove(IntersectedSectorsKey)
                del self.Sectors[IntersectedSectorsKey]
                self.DeletedSectors += 1
            
            #Add new Sector to PointTable and Sectors
            self.Sector = len(self.Sectors) + self.DeletedSectors
            for SectorPoint in Sector(*NewSectorPoints):
                print(SectorPoint)
                self.PointTable[SectorPoint].append((len(self.Sectors) + self.DeletedSectors))
            self.Sectors[len(self.Sectors) + self.DeletedSectors] = Sector(*NewSectorPoints)
        return
    def NewVector(self, NewVector):
        self.SolveNewVectorSectors(NewVector)

        ProposedVectorsDict = {}
        
        for VectorPointIndex in range(len(NewVector)):
            # Create New Vectors going from the point to all points in Sector
            ProposedVectorsFromPoint = dict(enumerate(map(lambda SectorPoint: Vector(NewVector[VectorPointIndex], SectorPoint), self.Sectors[self.Sector]), start=len(ProposedVectorsDict)))
            ProposedVectorsDict = {**ProposedVectorsDict, **ProposedVectorsFromPoint}

        VectorSets = set(map(frozenset, self.Sectors[self.Sector].Vectors))
        # Remove any intersecting Vectors
        for BlackKey in list(ProposedVectorsDict.keys()):
            # Create a list of ProposedVectorsDict that does not include BlackKey.
            # This means we will not Intersect BlackKey with itself and try and delete it
            blacklistdict = [WhiteValue for WhiteKey, WhiteValue in ProposedVectorsDict.items() if WhiteKey != BlackKey]
            blacklistdict.append(Vector(*NewVector))
            blacklistdict += self.Sectors[self.Sector].Vectors
            Intersection = list(filter(lambda ProposedPoint: VectorIntersectLinesNotPoints(*ProposedVectorsDict[BlackKey], *ProposedPoint), blacklistdict))
            if len(Intersection) > 0 or len(frozenset(ProposedVectorsDict[BlackKey]) & VectorSets) > 0:
                del ProposedVectorsDict[BlackKey]


        # Add NewVector to UserVectors and to Vectors
        NewUserVector = Vector(*NewVector)
        NewUserVector.Color = pygame.Color('red')
        self.Vectors[(0, len(self.UserVectors))] = NewUserVector
        self.UserVectors[len(self.UserVectors)] = NewUserVector

        # Reindex ProposedVectorsDict and add to ComputerVectors
        ProposedVectorsDict = dict(enumerate(ProposedVectorsDict.values(), start=len(self.ComputerVectors) + self.DeletedComputerVectors))
        self.ComputerVectors.update(ProposedVectorsDict)
        self.Vectors.update(dict(((1, Key), Value) for Key, Value in ProposedVectorsDict.items()))

        #Return a dict of all new vectors created so we can blit them to Pygame LineSurface
        self.CalculateSectors(NewVector, ProposedVectorsDict)
        return [Vector(*NewVector)] + list(ProposedVectorsDict.values())

    # Create new Sectors from new vector and the proposed computer vectors created from it
    def CalculateSectors(self, NewVector, ProposedVectorsDict):
        #ProposedVectorSets = list(map(lambda ProposedVectors: set(ProposedVectors), list(ProposedVectorsDict.values())))
        ProposedVectorSets = list(map(set, list(ProposedVectorsDict.values())))
        FoundSectors = []

        # Find Sectors bounded by a sector wall and a point in the NewVector
        for NewPoint in NewVector:
            Intersection = list(filter(lambda VectorPoint: 
            ((set((VectorPoint[0], NewPoint)) in ProposedVectorSets) and (set((VectorPoint[1], NewPoint)) in ProposedVectorSets)
             and not VectorIntersectLinesNotPoints(*VectorPoint, VectorPoint[0], NewPoint) and not VectorIntersectLinesNotPoints(*VectorPoint, VectorPoint[0], list({*NewVector} - {NewPoint})[0]))
             , self.Sectors[self.Sector].Vectors))

            for Index in Intersection:
                NewSector = set((*self.Sectors[self.Sector].Vectors[self.Sectors[self.Sector].Vectors.index(Index)], NewPoint))
                if NewSector not in FoundSectors:
                    FoundSectors.append(NewSector)

        # Find Sectors bounded by NewVector and a sector point
        for SectorPoint in self.Sectors[self.Sector]:
            if (set((SectorPoint, NewVector[0])) in ProposedVectorSets) and (set((SectorPoint, NewVector[1])) in ProposedVectorSets) and not VectorIntersectLinesNotPoints(*NewVector, NewVector[0], SectorPoint):
                NewSector = set((*NewVector, SectorPoint))
                if NewSector not in FoundSectors:
                    FoundSectors.append(NewSector)

        # Remove any sectors that have NewVector Points in them as this would overlap
        PointInSector = list(filter(lambda NewSector: IsPointInSectorNotPoints(Sector(*NewSector), NewVector[0]) or IsPointInSectorNotPoints(Sector(*NewSector), NewVector[1]), FoundSectors))
        for Index in PointInSector:
            del FoundSectors[FoundSectors.index(Index)]


        FoundSectors = list(map(lambda FoundSector: Sector(*FoundSector), FoundSectors))
        FoundDict = dict(enumerate(FoundSectors, start=len(self.Sectors) + self.DeletedSectors))


        # Now to remove current sector from the PointTable and remove it from dict of Sectors
        for OldSectorPoint in self.Sectors[self.Sector]:
            self.PointTable[OldSectorPoint].remove(self.Sector)
        del self.Sectors[self.Sector]
        self.DeletedSectors += 1
        self.Sector += 1

        for SectorKey, FoundSector in FoundDict.items():
            for SectorPoint in FoundSector:
                if SectorPoint in self.PointTable:
                    self.PointTable[SectorPoint].append(SectorKey)
                else:
                    self.PointTable[SectorPoint] = [SectorKey]



        self.Sectors.update(FoundDict)

        return FoundSectors




if __name__ == "__main__":
    import PointVectorSector as pvs
    print("Running main")

    # Points
    p1 = pvs.Point(0, 10)
    p2 = pvs.Point(10, 0)
    p3 = pvs.Point(10, 10)
    p4 = pvs.Point(0, 0)

    # Directly Perpendicular 
    v1 = pvs.Vector(p1, p2)
    v2 = pvs.Vector(p3, p4)

    # Parallel
    v3 = pvs.Vector(p1, p3)
    v4 = pvs.Vector(p2, p4)

    # Sectors
    s1 = pvs.Sector(p4, p1, p2)
    s2 = pvs.Sector(p1, p2, p3)




    

    


