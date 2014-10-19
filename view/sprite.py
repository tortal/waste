#  -*- coding: utf-8 -*-
# python 2.7.5
# author: roy.nard@gmail.com
# os: win32
import pygame

TILE_SIZE = 64


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)


class MapSprite(Sprite):
    def __init__(self, xy, group=None):
        Sprite.__init__(self, group)
        self.x, self.y = xy

        surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image = surf
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)

    def update(self, cameraPos):
        cX, cY = cameraPos
        x, y = (self.x - cX) * TILE_SIZE, (self.y - cY) * TILE_SIZE
        self.rect.x = x
        self.rect.y = y

    def saveSurf(self, surf):
        self.originalSurf = self.image.copy()

    def contains(self, xy):
        x, y = xy
        return self.rect.contains((x, y, 0, 0))

class ChestSprite(MapSprite):
    def __init__(self, xy, game, group=None):
        MapSprite.__init__(self, xy, group)
        self.game = game

        square = self.image.get_rect().inflate(-4, -4)
        pygame.draw.rect(self.image, (0, 150, 150), square)
        self.saveSurf(self.image)


class StartScreenBackgroundSprite(Sprite):
    def __init__(self, filePath, group=None):
        Sprite.__init__(self, group)

        img = pygame.image.load(filePath).convert()
        img.set_alpha(0)

        self.image = img
        self.rect = img.get_rect()


    def update(self):
        a = self.image.get_alpha()
        if a < 255:
            a += 1
            self.image.set_alpha(a)

    def isLoaded(self):
        return self.image.get_alpha() > 50


class GameScreenBackgroundSprite(Sprite):
    def __init__(self, group=None):
        Sprite.__init__(self, group)

        img = pygame.Surface((900, 600))
        img.fill((0, 0, 0))

        self.image = img
        self.rect = img.get_rect()

        #------------------------------------------------------------------------------


class BallSprite(Sprite):
    def __init__(self, group=None):
        Sprite.__init__(self, group)

        self.screenRect = pygame.display.get_surface().get_rect()
        self.moveSpeed = 1

        surf = pygame.Surface((64, 64))
        surf = surf.convert_alpha()
        surf.fill((0, 0, 0, 0))  #make transparent
        pygame.draw.circle(surf, (0, 0, 0), (32, 32), 32)
        self.image = surf
        self.rect = surf.get_rect()

        self.rect = self.rect.move((0, 400))

    #----------------------------------------------------------------------
    def update(self):
        newPos = self.rect.move((self.moveSpeed, 0))
        if self.rect.left < self.screenRect.left or self.rect.right > self.screenRect.right:
            self.moveSpeed = -self.moveSpeed
            newPos = self.rect.move((self.moveSpeed, 0))
        self.rect = newPos


class ObjectSprite(MapSprite):
    def __init__(self, xy, game, group=None):
        MapSprite.__init__(self, xy, group)
        self.game = game


class WallSprite(MapSprite):
    def __init__(self, xy, group=None):
        MapSprite.__init__(self, xy, group)

        square = self.image.get_rect().inflate(-4, -4)
        pygame.draw.rect(self.image, (0, 255, 0), square)
        self.saveSurf(self.image)   # TODO: What is this?


class FloorSprite(MapSprite):
    def __init__(self, xy, group=None):
        MapSprite.__init__(self, xy, group)

        square = self.image.get_rect().inflate(-4, -4)
        pygame.draw.rect(self.image, (255, 0, 0), square)
        self.saveSurf(self.image)


class ClickedTileSprite(MapSprite):
    def __init__(self, xy, group=None):
        MapSprite.__init__(self, xy, group)

        square = self.image.get_rect().inflate(-4, -4)
        pygame.draw.rect(self.image, (200, 200, 200, 50), square)
        self.saveSurf(self.image)


class EnemySprite(MapSprite):
    def __init__(self, xy, group=None):
        MapSprite.__init__(self, xy, group)

        self.square = self.image.get_rect().inflate(-4, -4)
        pygame.draw.rect(self.image, (100, 100, 100), self.square)
        self.saveSurf(self.image)


class ChestSprite(MapSprite):
    def __init__(self, xy, game, group=None):
        MapSprite.__init__(self, xy, group)
        self.game = game

        square = self.image.get_rect().inflate(-4, -4)
        pygame.draw.rect(self.image, (0, 150, 150), square)
        self.saveSurf(self.image)


class PlayerSprite(ObjectSprite):
    def __init__(self, game, group=None):
        xy = game.player.pos
        ObjectSprite.__init__(self, xy, game, group)

        square = self.image.get_rect().inflate(-4, -4)
        pygame.draw.rect(self.image, (255, 255, 255), square)

        self.saveSurf(self.image)

    def update(self, cameraPos):
        cX, cY = cameraPos
        x, y = self.game.player.pos

        self.rect.x = (x - cX) * TILE_SIZE
        self.rect.y = (y - cY) * TILE_SIZE


class DoorSprite(ObjectSprite):
    def __init__(self, xy, game, group=None):
        ObjectSprite.__init__(self, xy, game, group)

        self.square = self.image.get_rect().inflate(-4, -4)
        pygame.draw.rect(self.image, (0, 0, 255), self.square)

        self.saveSurf(self.image)

    def update(self, cameraPos):
        super(DoorSprite, self).update(cameraPos)
        doorTile = self.game.mapDict[self.x, self.y]

        if doorTile.isClosed:
            pygame.draw.rect(self.image, (0, 0, 255), self.square)
        else:
            pygame.draw.rect(self.image, (0, 0, 100), self.square)


class NextLevelSprite(ObjectSprite):
    def __init__(self, xy, game, group=None):
        ObjectSprite.__init__(self, xy, game, group)

        self.square = self.image.get_rect().inflate(-4, -4)
        pygame.draw.rect(self.image, (255, 255, 255), self.square)

        self.saveSurf(self.image)
