#  -*- coding: utf-8 -*-
# python 2.7.5
# author: roy.nard@gmail.com
# os: win32
import sys
import pygame
from pygame.locals import *
from cont import debug
from cont.event import EventBusClient, TickEvent, QuitEvent, KeyboardInputEvent, MouseInputEvent


class Clock(EventBusClient):
    """ Responsible for sending ticks to all other clients of the EventBus.
    """

    def __init__(self, eventBus, activated=1):
        EventBusClient.__init__(self, eventBus)
        self.FPS = 50
        self._timer = pygame.time.Clock()

        self.activated = activated
        self.tickEvent = TickEvent()  # Let's not create more than one of these...

    def run(self):
        while self.activated:
            self._timer.tick(self.FPS)
            self.eventBus.broadcast(self.tickEvent)
        debug.log('Clock: has been deactivated. Shutting Down.')
        pygame.quit()
        sys.exit(0)

    def update(self, event):
        if isinstance(event, QuitEvent):
            self.activated = False


class KeyboardController(EventBusClient):
    def __init__(self, eventBus):
        EventBusClient.__init__(self, eventBus)

    def update(self, event):
        if isinstance(event, TickEvent):
            self._handleInputEvents()

    def _handleInputEvents(self):
        for e in pygame.event.get():
            if e.type == QUIT:
                self.eventBus.broadcast(QuitEvent())
            elif e.type == KEYUP and e.key == K_ESCAPE:
                self.eventBus.broadcast(QuitEvent())
            elif e.type == KEYUP:
                self.eventBus.broadcast(KeyboardInputEvent(e.key))
            elif e.type == MOUSEBUTTONUP:
                self.eventBus.broadcast(MouseInputEvent(1, e.pos))
