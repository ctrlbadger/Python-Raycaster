import pygame
from PointVectorSector import *
from Graphics import *
import pygame.gfxdraw
"""
def VectorIntersect(Vector1, Vector2):

    PositionVector1 = (Vector1[1]-Vector1[0])
    PositionVector2 = (Vector2[1]-Vector2[0])
    RatioVector1 = ((Vector1[0]^PositionVector1)-(Vector2[0]^PositionVector1))/(PositionVector2^PositionVector1)
    print("Ratio Vector1", RatioVector1)
    RatioVector2 = ((Vector2[0]^PositionVector2)-(Vector1[0]^PositionVector2))/(PositionVector1^PositionVector2)
    print("Ratio Vector2", RatioVector2)
    if (0 <= RatioVector1 <= 1) and (0 <= RatioVector1 <= 1):
        return True
    else:
        return False
"""
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

def IsTriangleClockwise(Point1, Point2, Point3):
    return (Point2-Point1)^(Point3-Point1) > 0


def IsPointInTriangle(Point1, Point2, Point3, Point4):
    Orientation1 = (Point2 - Point1)^(Point4 - Point1)
    Orientation2 = (Point3 - Point2)^(Point4 - Point2)
    Orientation3 = (Point1 - Point3)^(Point4 - Point3)
    return ((Point2-Point1)^(Point3-Point1) > 0) and (Orientation1 > 0 and Orientation2 > 0 and Orientation3 > 0)




class Map():
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
        """
        Sectors has a list of all Sector objects
        Sector has a list of Points in that Sector

        Points have a list of all Vectors that use it
        """
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
graphics = Graphics([1000, 1000])

ScaleFactor = 100
Offset = Point(-50, -50)
WorldSize = [10, 10]
graphics.DrawGrid(ScaleFactor, WorldSize, Offset)
VectorMap = Map(WorldSize)


IsDragging = False
while True:
    events = pygame.event.get()

    for event in events:

        if event.type == pygame.QUIT:
            pygame.quit()
        # Is mouse moving? If mousing over a dot then colour
        # Get the new position of the mouse and draw it on screen
        # If Dragging then move a line to the mouse prosition
        if event.type == pygame.MOUSEMOTION:
            graphics.MouseSprite.ChangeText(str(pygame.mouse.get_pos()), pygame.Color('black'))
            graphics.IsMouseOverGrid(10)
            if IsDragging == True:
                graphics.LineDrag.UpdatePoint2(Point(*pygame.mouse.get_pos()))
            graphics.DrawSprites()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            GetPos = graphics.IsMouseOverGrid(10)
            if GetPos != []:
                graphics.DotDragSprites.append(graphics.DotHighlightSprites[-1])
                GetPos = GetPos[0]
                GridX = int((GetPos.x + Offset.x)/ScaleFactor)
                GridY = int((GetPos.y + Offset.y)/ScaleFactor)
                print(Point(GridX, GridY))
                IsDragging = True
                graphics.LineDrag = Line(GetPos, Point(*pygame.mouse.get_pos()), pygame.Color('green'))
                graphics.DirtySprites.add(graphics.LineDrag)
                graphics.DrawSprites()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            GetPos = graphics.IsMouseOverGrid(10)
            #
            if GetPos != []:
                GetPos = GetPos[0]
                #Work out which part of the grid he is in
                OriginalPoint = (graphics.LineDrag.Point1 + Offset) / ScaleFactor

                GridX = int((GetPos.x + Offset.x)/ScaleFactor)
                GridY = int((GetPos.y + Offset.y)/ScaleFactor)
                print(Point(GridX, GridY))
                NewVectors = VectorMap.NewVector((OriginalPoint, Point(GridX, GridY) ))
                graphics.DrawNewLines(NewVectors, ScaleFactor, Offset)

            graphics.DirtySprites.remove(graphics.DotDragSprites)
            graphics.DirtySprites.remove(graphics.LineDrag)
            graphics.DotDragSprites = []
            graphics.LineDrag = None
            IsDragging = False
            graphics.DrawSprites()
        #elif event.type != pygame.MOUSEBUTTONDOWN and event.button == 1:
        #print("This your moment!")
