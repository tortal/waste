#  -*- coding: utf-8 -*-
# python 2.7.5
# author: roy.nard@gmail.com
# os: win32

import pygame
from cont import debug
from cont.event import EventBusClient, TickEvent, ShowScreenEvent, PlaySoundEvent
import color
from screen import StartScreen


class GameView(EventBusClient):
    def __init__(self, eventBus, windowSize, windowCaption):

        EventBusClient.__init__(self, eventBus)

        self.screen = None
        self.windowSize = windowSize

        pygame.display.init()
        self.mainSurf = pygame.display.set_mode(self.windowSize)
        pygame.display.set_caption(windowCaption)

        self.size = self.mainSurf.get_size()

        # "Loading Screen"
        self.backgroundSurf = pygame.Surface(self.windowSize)
        self.backgroundSurf.fill(color.BLACK)
        pygame.display.flip()


    def draw(self):
        if not self.screen:
            return
        self.screen.draw(self.mainSurf)

    def update(self, event):
        if isinstance(event, TickEvent):
            self.draw()
        elif isinstance(event, ShowScreenEvent):
            if self.screen:
                self.eventBus.removeClient(self.screen)
            self.screen = event.content


class Sound(EventBusClient):
    def __init__(self, eventBus, config):
        EventBusClient.__init__(self, eventBus)
        self.config = config

        freq = 44100
        bits = -16
        channels = 2
        buffer = 1024
        volume = 0.4

        # Initialize audio mixer
        pygame.mixer.init(freq, bits, channels, buffer)
        pygame.mixer.music.set_volume(volume)

    def update(self, event):
        if isinstance(event, ShowScreenEvent) and isinstance(event.content, StartScreen):
            pygame.mixer.music.load(self.config['StartScreen']['music_path'])
            pygame.mixer.music.play(-1)
            debug.log('playing:', self.config['StartScreen']['music_path'])
        if isinstance(event, PlaySoundEvent):
            sound = pygame.mixer.Sound(event.content)
            sound.play()