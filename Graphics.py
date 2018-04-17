import pygame.gfxdraw
import pygame
from PointVectorSector import *

class Graphics():
    def __init__(self, ScreenResolution):
        pygame.init()
        self.Surface = pygame.display.set_mode(ScreenResolution)
        self.LineSurface = pygame.Surface(self.Surface.get_size()).convert_alpha()
        self.LineSurface.fill((255, 255, 255, 0), None, pygame.BLEND_RGBA_MULT)

        self.ScreenResolution = ScreenResolution
        self.DefaultFont = pygame.font.get_default_font()


        self.MouseSprite = Text("MousePosition", 20, pygame.Color('Black'), 1000, 20)
        self.LineSprites = []
        self.LineDrag = None

        self.DotSprites = []
        self.DotHighlightSprites = []
        self.DotDragSprites = []
        self.DirtySprites = pygame.sprite.LayeredDirty(self.MouseSprite)

        self.Grid = []

    def DrawGrid(self, ScaleFactor, GridSize, Offset):
        self.Background = pygame.Surface(self.Surface.get_size())
        self.Background.fill(pygame.Color('white'))
        for x in range(GridSize[0]):
            for y in range(GridSize[1]):
                XCoordinate = (x) * ScaleFactor - Offset.x
                YCoordinate = (y) * ScaleFactor - Offset.y
                self.Grid.append(Point(XCoordinate, YCoordinate))
                pygame.gfxdraw.filled_circle(self.Background, XCoordinate, YCoordinate, 4, pygame.Color('black'))
        self.Surface.blit(self.Background, self.Background.get_rect())
        pygame.display.update(self.Background.get_rect())
    def DrawSprites(self):
        self.DirtySprites.clear(self.Surface, self.Background)
        self.DirtySprites.update()
        Rects = self.DirtySprites.draw(self.Surface)
        pygame.display.update(Rects)
    def IsMouseOverGrid(self, radius):
        Cursor = Point(*pygame.mouse.get_pos())

        FocusedPoint = list(filter(lambda Point: True if ((Point.x - radius) <= Cursor.x <= (Point.x + radius)) and ((Point.y - radius) <= Cursor.y <= (Point.y + radius)) else False, self.Grid))
        if FocusedPoint != []:
            AlreadySprite = False
            for DotSpritesIndex in range(len(self.DotHighlightSprites)):
                if self.DotHighlightSprites[DotSpritesIndex].Point == FocusedPoint[0]:
                    AlreadySprite = True
                    break
            if not AlreadySprite:
                DotSprite = Dot(FocusedPoint[0].x, FocusedPoint[0].y, 4, pygame.Color("red"))
                self.DotHighlightSprites.append(DotSprite)
                self.DirtySprites.add(DotSprite)
        else:
            if self.DotHighlightSprites != []:
                if (self.DotHighlightSprites[-1] in self.DotDragSprites):
                    self.DotHighlightSprites = []
                else:
                    self.DirtySprites.remove(self.DotHighlightSprites)
                    self.DotHighlightSprites = []

        return FocusedPoint
    def DrawNewLines(self, VectorList, ScalingFactor, Offset):
        VectorRects = []
        for VectorLine in VectorList:
            if VectorLine.Color == None:
                VectorLine.Color = pygame.Color('grey')
            ScaledVector1 = ((VectorLine[0] * ScalingFactor) - Offset).PointToIntPoint()
            ScaledVector2 = ((VectorLine[1] * ScalingFactor) - Offset).PointToIntPoint()
            ScaledVector1.PointToIntPoint()
            ScaledVector2.PointToIntPoint()

            pygame.gfxdraw.line(self.LineSurface, *ScaledVector1, *ScaledVector2, VectorLine.Color)
            SortX = sorted([ScaledVector1.x, ScaledVector2.x])
            SortY = sorted([ScaledVector1.y, ScaledVector2.y])
            VectorRects.append(pygame.Rect(SortX[0], SortY[0], (SortX[1]-SortX[0]), (SortY[1]-SortY[0])))
            self.Background.blit(self.LineSurface, self.LineSurface.get_rect())
        pygame.display.update()
    def RemoveLines(self, VectorList, ScalingFactor, Offset):
        VectorRects = []
        for VectorLine in VectorList:
            ScaledVector1 = ((VectorLine[0] * ScalingFactor) - Offset).PointToIntPoint()
            ScaledVector2 = ((VectorLine[1] * ScalingFactor) - Offset).PointToIntPoint()
            ScaledVector1.PointToIntPoint()
            ScaledVector2.PointToIntPoint()

            pygame.gfxdraw.line(self.LineSurface, *ScaledVector1, *ScaledVector2, pygame.Color('white'))
            SortX = sorted([ScaledVector1.x, ScaledVector2.x])
            SortY = sorted([ScaledVector1.y, ScaledVector2.y])
            VectorRects.append(pygame.Rect(SortX[0], SortY[0], (SortX[1]-SortX[0]), (SortY[1]-SortY[0])))
            self.Background.blit(self.LineSurface, self.LineSurface.get_rect())
        pygame.display.update()
class Dot(pygame.sprite.DirtySprite):
    def __init__(self, XCoordinate, YCoordinate, Radius, Colour):
        self.Point = Point(XCoordinate, YCoordinate)
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface((Radius*2, Radius*2)).convert_alpha()
        self.image.fill(pygame.Color(255, 255, 255, 0))
        pygame.gfxdraw.filled_circle(self.image, Radius, Radius, Radius, Colour)
        self.rect = pygame.Rect(XCoordinate-Radius, YCoordinate-Radius, 2*Radius, 2*Radius)
        self.dirty = 0
        self.visible = 1
    def update(self):
         self.dirty = 1
class Text(pygame.sprite.DirtySprite):
    def __init__(self, text, size, color, width,  height):
        self.width = width
        self.height = height
        pygame.sprite.DirtySprite.__init__(self)
        self.font = pygame.font.SysFont("Arial", size)
        self.textSurf = self.font.render(text, True, color)
        self.image = pygame.Surface((width, height)).convert_alpha()
        alpha = 0
        self.image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)

        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [width/2 - W/2, height/2 - H/2])
        self.rect = self.image.get_rect()

    def ChangeText(self, text, color):
        self.textSurf = self.font.render(text, True, color)
        alpha = 0
        self.image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [self.width/2 - W/2, self.height/2 - H/2])
        self.dirty = 1
class Line(pygame.sprite.DirtySprite):
    def __init__(self, Point1, Point2, Colour):
        self.Point1 = Point1
        self.Point2 = Point2
        self.Colour = Colour
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface((1000, 1000)).convert_alpha()
        self.image.fill((255, 255, 255, 0), None, pygame.BLEND_RGBA_MULT)
        pygame.gfxdraw.line(self.image, *Point1, *Point2, Colour)
        self.rect = self.image.get_rect()
        self.dirty = 0
    def UpdatePoint2(self, Point2):
        self.Point2 = Point2
        self.image = pygame.Surface((1000, 1000)).convert_alpha()
        self.image.fill((255, 255, 255, 0), None, pygame.BLEND_RGBA_MULT)
        pygame.gfxdraw.line(self.image, *self.Point1, *self.Point2, self.Colour)
        self.rect = self.image.get_rect()
        self.dirty = 1
