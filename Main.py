import pygame
from PointVectorSector import *
from Graphics import *
from Map import *
import pygame.gfxdraw

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
                OriginalPoint = (graphics.LineDrag.Point1 + Offset) / ScaleFactor
                GridX = int((GetPos.x + Offset.x)/ScaleFactor)
                GridY = int((GetPos.y + Offset.y)/ScaleFactor)
                # Create any new vectors that need to be created
                NewVectors = VectorMap.NewVector((OriginalPoint, Point(GridX, GridY) ))
                graphics.DrawNewLines(NewVectors, ScaleFactor, Offset)

            graphics.DirtySprites.remove(graphics.DotDragSprites)
            graphics.DirtySprites.remove(graphics.LineDrag)
            graphics.DotDragSprites = []
            graphics.LineDrag = None
            IsDragging = False
            graphics.DrawSprites()
