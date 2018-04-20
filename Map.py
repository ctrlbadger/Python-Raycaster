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




def IsTriangleClockwise(Point1, Point2, Point3):
    """Checks if the Triangle created by Point1, Point2 and Point3 Intersect"""
    return (Point2-Point1)^(Point3-Point1) >= 0


def IsPointInTriangle(Point1, Point2, Point3, Point4):
    """
    Check if Point4 is in Triangle bounded by Point1, Point2, Point3
    Used to check if a point is in a given sector
    """
    Orientation1 = (Point2 - Point1)^(Point4 - Point1)
    Orientation2 = (Point3 - Point2)^(Point4 - Point2)
    Orientation3 = (Point1 - Point3)^(Point4 - Point3)
    return ((Point2-Point1)^(Point3-Point1) < 0) and (Orientation1 < 0 and Orientation2 < 0 and Orientation3 < 0)



def IsPointInSector(Sector1, CheckPoint):
    """Checks if a Point is in a Sector, also checks the lines bounded by the Sector"""
    Orientations = [((Sector1[Index] - Sector1[(Index - 1) % len(Sector1)]) ^ (CheckPoint - Sector1[(Index - 1) % len(Sector1)])) for Index in range(len(Sector1))]
    if (((Sector1[1]-Sector1[0])^(Sector1[2]-Sector1[0])) < 0):
        return len(list(filter(lambda Orientation: Orientation > 0, Orientations))) == 0
    else:
        return len(list(filter(lambda Orientation: Orientation < 0, Orientations))) == 0


def IsPointInSectorNoLines(Sector1, CheckPoint):
    """"Checks if a point is inside a sector, does not check lines of sector"""
    Orientations = [((Sector1[Index] - Sector1[(Index - 1) % len(Sector1)]) ^ (CheckPoint - Sector1[(Index - 1) % len(Sector1)])) for Index in range(len(Sector1))]
    if (((Sector1[1]-Sector1[0])^(Sector1[2]-Sector1[0])) < 0):
        return len(list(filter(lambda Orientation: Orientation >= 0, Orientations))) == 0
    else:
        return len(list(filter(lambda Orientation: Orientation <= 0, Orientations))) == 0

def IsPointInSectorNoLinesButPoints(Sector1, CheckPoint):
    """"Checks if a point is inside a sector, does not check lines of sector but does check Points"""
    if any(map(lambda sPoint: sPoint == CheckPoint, Sector1)):
        return True
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
        self.UserVectors = []
        self.DeletedUserVectors = 0

        #self.ComputerVectors = {}
        self.DeletedComputerVectors = 0

        # Just going to hard code in the First sector might channge it later
        self.Sectors = {0: Sector(Point(0, 0), Point(9,0), Point(9, 9), Point(0,9))}
        self.DeletedSectors = 0
        self.RemovedVectors = []

        self.PointTable = {Point(0, 0): {0}, Point(9,0): {0}, Point(0,9): {0}, Point(9, 9): {0}}
        #self.ComputerVectors = dict(enumerate(self.Sectors[self.Sector].Vectors))
        
        #self.Vectors.update(dict(((1, Key), Value) for Key, Value in self.ComputerVectors.items()))

    # Try and locate a point, will search any sectors around it and then every sector. Yes I know it's not that efficient
    def FindNewSector(self, CheckSector, CheckPoint):
        # Find all adjacent sectors
        AdjacentSectors = [self.PointTable[CheckSectorPoint] for CheckSectorPoint in self.Sectors[CheckSector]]
        NewSet = set([item for items in AdjacentSectors for item in items]) - set(CheckPoint)

        # Check if point is in Adjacent sectors
        for PossibleSector in list(NewSet):
            if IsPointInSector(self.Sectors[PossibleSector], CheckPoint): return PossibleSector

        #Huh that's odd guess we are going to have to go on a goose chase to find this one
        for PossibleSector in self.Sectors.keys():
            if IsPointInSector(self.Sectors[PossibleSector], CheckPoint): return PossibleSector

        #Might be out of range so best to leave it alone
        return CheckSector

    def SolveNewVectorSectors(self, NewVector):
        NewVectorSectorIntersects = []
        for NewPoint in NewVector:
            SectorPointDict = set([SectorKey for SectorKey, SectorValue in self.Sectors.items() if IsPointInSectorNoLinesButPoints(SectorValue, NewPoint)])
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
                self.PointTable[SectorPoint].add((len(self.Sectors) + self.DeletedSectors))
            self.Sectors[len(self.Sectors) + self.DeletedSectors] = Sector(*NewSectorPoints)
        return

    def CutSector(self, lZippedCheckVectorPoints, iCurrent, vCreated):
        """
        Cuts the sector where the Vector intersects the edge
        """
        lIndexCheckVectorPoints = [index for index, item in enumerate(lZippedCheckVectorPoints[0]) if item == False]
        for index in lIndexCheckVectorPoints:
            if lZippedCheckVectorPoints[1][index] != True: # We need to modify the Sector.
                for indexVector, sectorVector in enumerate(self.Sectors[iCurrent].Vectors):
                    # If this is the specific vector that has been intersected
                    # Insert the point just after it
                    if VectorIntersectLinesNotPoints(*sectorVector, sectorVector[0], vCreated[index]):
                        self.Sectors[iCurrent].insert((indexVector + 1) % len(self.Sectors[iCurrent]), vCreated[index])
                        self.PointTable[vCreated[index]] = {iCurrent}
        return

    def NewVector(self, vCreated):
        # First need to establish what the condition of the Vector is.
        """
        if   vCreated is only in one sector
        elif VCreated is only in one sector but with points touching edges
        elif VCreated is only in one sector with points touching sector points
        elif VCreated is in multiple sectors with no points touching edges
        elif VCreated is in multiple sectors with points touching edges
        elif vCreated is in multiple sectors with points touching sector points
        """

        # First find the index of Sectors for which vCreated has points in
        dProposedVectors = dict
        dSectorKeys = {key: sItem for key, sItem in self.Sectors.items() if \
            any(map(lambda vectorPoint: IsPointInSector(sItem, vectorPoint), vCreated))}

        
        if len(dSectorKeys) == 1: # If only one sector was found
            iCurrent, sCurrent = dSectorKeys.popitem()
            """
            lCheckVectorPoints = [[IsPointInSectorNoLines(sCurrent, vectorPoint), IsPointInSectorNoLinesButPoints(sCurrent, vectorPoint)] \
                for vectorPoint in vCreated]
            lZippedCheckVectorPoints = list(map(list, zip(*lCheckVectorPoints)))
            """

            lNoLines = [IsPointInSectorNoLines(sCurrent, vectorPoint) for vectorPoint in vCreated]
            lNoLinesButPoints = [IsPointInSectorNoLinesButPoints(sCurrent, vectorPoint) for vectorPoint in vCreated]
            lZippedCheckVectorPoints = [lNoLines, lNoLinesButPoints]
            
            if not all(lZippedCheckVectorPoints[0]): # We might need to split up the sector
                self.CutSector(lZippedCheckVectorPoints, iCurrent, vCreated)
            dProposedVectors = self.CreateVectorsSingle(iCurrent, vCreated)
        else:
            # So the time I tried this last I had a migrane just looking at the code
            # The task is to break up sectors into larger sectors

            # Find weird sectors that need breaking up
            for sectorKey, sectorItem in dSectorKeys.items():
                for pCreated in vCreated:
                    for indexVectorPoint, sectorVector in enumerate(sectorItem.Vectors):          
                        if VectorIntersectLinesNotPoints(*sectorVector, sectorVector[0], pCreated): # and pCreated not in sectorVector:
                            sectorItem.insert((indexVectorPoint + 1) % len(self.Sectors[sectorKey]), pCreated)
                            if pCreated not in self.PointTable:
                                self.PointTable[pCreated] = {sectorKey}
                            else:
                                self.PointTable[pCreated].add(sectorKey)




        
        self.CalculateSectors(vCreated, dProposedVectors)
        # dProposedVectors = {key: Vector(item) for key, item in dProposedVectors.items()}
        self.UserVectors.append(Vector(*vCreated))
        self.UserVectors[-1].Color = 'red'
        return [self.UserVectors[-1]] + list(map(lambda x: Vector(*x), dProposedVectors.values()))

    def CreateVectorsSingle(self, iCurrent, vCreated):
        lProposedVectors = []
        lCurrentSectorVectors = set((map(frozenset, self.Sectors[iCurrent].Vectors), frozenset(vCreated)))
        for indexPoint, vectorPoint in enumerate(vCreated):
            lProposedVectors += [frozenset((vectorPoint, sectorPoint)) for sectorPoint in self.Sectors[iCurrent] if \
                {vectorPoint, sectorPoint} not in lCurrentSectorVectors and \
                not VectorIntersectLinesNotPoints(vectorPoint, sectorPoint, vectorPoint, vCreated[(indexPoint + 1) % 2])]
            
        dProposedVectors = dict(enumerate(lProposedVectors))
        for index, currentVector in dict(dProposedVectors.items()).items():
            whitelist = set(dProposedVectors.values()) - currentVector
            for whitevector in whitelist:
                if VectorIntersectLinesNotPoints(*whitevector, *currentVector):
                    del dProposedVectors[index]
                    break


        dProposedVectors = dict(enumerate(dProposedVectors.values()))
        return dProposedVectors
        
                

    # Create new Sectors from new vector and the proposed computer vectors created from it
    def CalculateSectors(self, NewVector, ProposedVectorsDict):
        #ProposedVectorSets = list(map(lambda ProposedVectors: set(ProposedVectors), list(ProposedVectorsDict.values())))
        ProposedVectorSets = list(map(set, list(ProposedVectorsDict.values())))
        FoundSectors = []

        # Find Sectors bounded by a sector wall and a point in the NewVector
        for NewPoint in NewVector:
            Intersection = list(filter(lambda VectorPoint: \
                ((set((VectorPoint[0], NewPoint)) in ProposedVectorSets) and \
                (set((VectorPoint[1], NewPoint)) in ProposedVectorSets)  and \
                not VectorIntersectLinesNotPoints(*VectorPoint, VectorPoint[0], NewPoint) and \
                not VectorIntersectLinesNotPoints(*VectorPoint, VectorPoint[0], list({*NewVector} - {NewPoint})[0])), \
                self.Sectors[self.Sector].Vectors))

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
        PointInSector = list(filter(lambda NewSector: IsPointInSectorNoLines(Sector(*NewSector), NewVector[0]) or IsPointInSectorNoLines(Sector(*NewSector), NewVector[1]), FoundSectors))
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
                    self.PointTable[SectorPoint].add(SectorKey)
                else:
                    self.PointTable[SectorPoint] = {SectorKey}



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

    print(VectorIntersectLinesNotPoints(p4, p1, p4, p4))

    p5 = pvs.Point(5, 5)
    p6 = pvs.Point(5, 0)

    # Directly Perpendicular 
    v1 = pvs.Vector(p1, p2)
    v2 = pvs.Vector(p3, p4)

    # Parallel
    v3 = pvs.Vector(p1, p3)
    v4 = pvs.Vector(p2, p4)

    # Sectors
    s1 = pvs.Sector(p4, p1, p2)
    s2 = pvs.Sector(p1, p2, p3)
    s3 = pvs.Sector(p1, p3, p2, p4)

    print(s3, p5, IsPointInSectorNoLines(s3, p5))
    print(s3, p4, IsPointInSectorNoLinesButPoints(s3, p4))

    

    


