import pygame
import pygame.gfxdraw

from Graphics import *
from Map import *
from PointVectorSector import *

graphics = Graphics([1000, 1000])

SCALE_FACTOR = 100
OFFSET = Point(-50, -50)
WORLD_SIZE = [10, 10]
graphics.DrawGrid(SCALE_FACTOR, WORLD_SIZE, OFFSET)
VectorMap = Map(WORLD_SIZE)

# Relative Position
def RelativePosition(PositionPoint, ScaleFactor, Offset):
    return (PositionPoint + Offset) / ScaleFactor


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
            MousePosition = Point(*pygame.mouse.get_pos())
            MapMousePosition = RelativePosition(MousePosition, SCALE_FACTOR, OFFSET)
            # So let's implement some more checks so we know where we are
            if not IsPointInSectorAndPoints(VectorMap.Sectors[VectorMap.Sector], MapMousePosition):
                VectorMap.Sector = VectorMap.FindNewSector(VectorMap.Sector, MapMousePosition)
            graphics.MouseSprite.ChangeText(str(MousePosition)+str(RelativePosition(MousePosition, SCALE_FACTOR, OFFSET))+str(VectorMap.Sector), pygame.Color('black'))
            graphics.IsMouseOverGrid(10)
            if IsDragging:
                graphics.LineDrag.UpdatePoint2(Point(*pygame.mouse.get_pos()))
            graphics.DrawSprites()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            GetPos = graphics.IsMouseOverGrid(10)
            if GetPos != []:
                graphics.DotDragSprites.append(graphics.DotHighlightSprites[-1])
                GetPos = GetPos[0]
                GridX = int((GetPos.x + OFFSET.x)/SCALE_FACTOR)
                GridY = int((GetPos.y + OFFSET.y)/SCALE_FACTOR)
                IsDragging = True
                graphics.LineDrag = Line(GetPos, Point(*pygame.mouse.get_pos()), pygame.Color('green'))
                graphics.DirtySprites.add(graphics.LineDrag)
                graphics.DrawSprites()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            GetPos = graphics.IsMouseOverGrid(10)
            #
            if GetPos != []:
                GetPos = GetPos[0]
                # Rescale the points to fit the grid size
                OriginalPoint = (graphics.LineDrag.Point1 + OFFSET) / SCALE_FACTOR
                GridX = int((GetPos.x + OFFSET.x)/SCALE_FACTOR)
                GridY = int((GetPos.y + OFFSET.y)/SCALE_FACTOR)
                # Create any new vectors that need to be created
                NewVectors = VectorMap.NewVector((OriginalPoint, Point(GridX, GridY)))
                graphics.DrawNewLines(NewVectors, SCALE_FACTOR, OFFSET)

            graphics.DirtySprites.remove(graphics.DotDragSprites)
            graphics.DirtySprites.remove(graphics.LineDrag)
            graphics.DotDragSprites = []
            graphics.LineDrag = None
            IsDragging = False
            graphics.DrawSprites()
