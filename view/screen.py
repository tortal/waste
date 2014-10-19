#  -*- coding: utf-8 -*-
# python 2.7.5
# author: roy.nard@gmail.com
# os: win32
import pygame
from cont.event import EventBusClient, KeyboardInputEvent, ShowScreenEvent, MouseInputEvent, GameOverEvent
from model.game import GameModel
from sprite import \
    StartScreenBackgroundSprite, BallSprite, GameScreenBackgroundSprite
from spritegroups import MapSpritesGroup, ObjectSpritesGroup, OverlaySpritesGroup


class Screen(EventBusClient):
    """ A screen that can be added to GameView, like menu, gameview, inventory """

    def __init__(self, eventBus, config):
        EventBusClient.__init__(self, eventBus)

        self.type = 'Base View Component'
        self.config = config

        self.backSprites = pygame.sprite.RenderUpdates()
        self.mapSprites = pygame.sprite.RenderUpdates()


class StartScreen(Screen):
    def __init__(self, eventBus, assets):
        Screen.__init__(self, eventBus, assets)

        #img = sprite.BackgroundSprite(self.assets['StartScreen']['background_image_path'], self.backSprites)
        #self.backgroundSurf = pygame.image.load(self.assets['StartScreen']['background_image_path']).convert()
        self._startScreenSprite = StartScreenBackgroundSprite(self.config['StartScreen']['bgimage_path'], self.backSprites)
        self.backgroundSurf = self._startScreenSprite.image

        #pygame.display.get_surface().blit(self.backgroundSurf, (0,0))
        spr = BallSprite(self.mapSprites)

    def draw(self, mainSurf):
        self.backSprites.clear(mainSurf, self.backgroundSurf)
        self.mapSprites.clear(mainSurf, self.backgroundSurf)

        self.backSprites.update()
        self.mapSprites.update()

        dirtyRectList1 = self.backSprites.draw(mainSurf)       # remove list()
        dirtyRectList2 = self.mapSprites.draw(mainSurf)

        allDirtyRect = dirtyRectList1 + dirtyRectList2
        pygame.display.update(allDirtyRect)

    def update(self, event):
        if isinstance(event, KeyboardInputEvent) and self._startScreenSprite.isLoaded():
            self.eventBus.broadcast(ShowScreenEvent(GameScreen(self.eventBus, self.config)))



class GameScreen(Screen):
    """ The main game screen
    """
    # Coordinate offset to center tile on screen (d = 0,0 will center at top-left corner)
    dx = -7
    dy = -4

    def __init__(self, eventBus, config):
        Screen.__init__(self, eventBus, config)
        self.game = GameModel(eventBus, config)


        x, y = self.game.player.pos
        self.cameraXY = x + GameScreen.dx, y + GameScreen.dy
        spr = GameScreenBackgroundSprite(self.backSprites)
        self.backgroundSurf = spr.image

        self.mapSprites = MapSpritesGroup()
        self.mapSprites.loadSprites(self.game)

        self.objectSprites = ObjectSpritesGroup()
        self.objectSprites.loadSprites(self.game)

        self.mapSprites = MapSpritesGroup()
        self.mapSprites.loadSprites(self.game)

        self.overlaySprites = OverlaySpritesGroup()

        self.allSprites = self.objectSprites.sprites() + self.mapSprites.sprites()

    def draw(self, mainSurf):

        self.backSprites.clear(mainSurf, self.backgroundSurf)
        self.mapSprites.clear(mainSurf, self.backgroundSurf)
        self.objectSprites.clear(mainSurf, self.backgroundSurf)
        self.overlaySprites.clear(mainSurf, self.backgroundSurf)

        self.backSprites.update()
        self.mapSprites.update(self.cameraXY)
        self.objectSprites.update(self.cameraXY)
        self.overlaySprites.update(self.cameraXY)

        rects1 = self.backSprites.draw(mainSurf)
        rects2 = self.mapSprites.draw(mainSurf)
        rects3 = self.objectSprites.draw(mainSurf)
        rects4 = self.overlaySprites.draw(mainSurf)

        allDirtyRect = rects1 + rects2 + rects3 + rects4
        pygame.display.update(allDirtyRect)

    def update(self, e):
        if isinstance(e, MouseInputEvent):
            sprites = self.mapSprites.sprites() + self.objectSprites.sprites()
            for s in sprites:
                if s.contains(e.pos):
                    print 'You see a', s.__class__.__name__
        x, y = self.game.player.pos
        self.cameraXY = x + GameScreen.dx, y + GameScreen.dy

        if isinstance(e, GameOverEvent):

            print e.content
            print """
            #########################################################
            #########################################################

            GAME OVER!!!

            YOU STEP COUNT WAS %d
            """ % e.content
            newEvent = ShowScreenEvent(StartScreen(self.eventBus, self.config))
            self.eventBus.broadcast(newEvent)