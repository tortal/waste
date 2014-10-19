import pygame
from model.tile import FloorTile, WallTile, DoorTile, PlayerStartTile, ChestTile, NextLevelTile
from sprite import FloorSprite, WallSprite, DoorSprite, PlayerSprite, ChestSprite, ClickedTileSprite
from sprite import NextLevelSprite


class SpritesGroup(pygame.sprite.RenderUpdates):
    def __init__(self, *sprites):
        pygame.sprite.RenderUpdates.__init__(self, *sprites)
        self.game = None
        #self.cameraX, self.cameraY = 0, 0

    def update(self, cameraXY):
        for s in self.sprites():
            s.update(cameraXY)


class MapSpritesGroup(SpritesGroup):
    def __init__(self, *sprites):
        SpritesGroup.__init__(self, sprites)

    def loadSprites(self, game):
        self.empty()
        self.game = game
        gameMap = game.mapDict
        for xy, tile in gameMap.iteritems():
            if isinstance(tile, FloorTile):
                FloorSprite(xy, self)
            elif isinstance(tile, WallTile):
                WallSprite(xy, self)
            elif isinstance(tile, DoorTile):
                DoorSprite(xy, game, self)
            elif isinstance(tile, NextLevelTile):
                NextLevelSprite(xy, game, self)

class ObjectSpritesGroup(MapSpritesGroup):
    def __init__(self, *sprites):
        MapSpritesGroup.__init__(self, *sprites)

    def loadSprites(self, game):
        self.empty()

        for xy, tile in game.mapDict.iteritems():
            if isinstance(tile, PlayerStartTile):
                PlayerSprite(game, self)
            elif isinstance(tile, ChestTile):
                ChestSprite(xy, game, self)

    def update(self, cameraXY):
        super(ObjectSpritesGroup, self).update(cameraXY)

class OverlaySpritesGroup(SpritesGroup):
    def __init__(self, *sprites):
        SpritesGroup.__init__(self, sprites)

    def onClick(self, xy, sprite):
            if sprite.contains(xy):
                print 'you clicked', sprite.__class__.__name__
                xy = sprite.x, sprite.y