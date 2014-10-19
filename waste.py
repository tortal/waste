#  -*- coding: utf-8 -*-
# python 2.7.5
# author: roy.nard@gmail.com
# os: win32
from cont import debug
from cont.resources import Assets
from cont.controller import KeyboardController, Clock
from cont.event import EventBus, EventBusClient, ShowScreenEvent
from view.screen import StartScreen
from view.view import GameView, Sound

#####################################################################
def main():
    debug.enableDebug = False

    eventBus = EventBus()
    KeyboardController(eventBus)
    GameView(eventBus, (900, 600), 'Waste')

    fileAssets = Assets()
    config = fileAssets.config
    Sound(eventBus, config)

    startScreen = StartScreen(eventBus, config)
    debugClient = DebugClient(eventBus)
    debugClient.broadcast(ShowScreenEvent(startScreen))

    debug.log('all listeners;', eventBus.listeners)
    Clock(eventBus).run()

#####################################################################

class DebugClient(EventBusClient):
    def __init__(self, eventBus):
        EventBusClient.__init__(self, eventBus)

    def broadcast(self, event):
        self.eventBus.broadcast(event)

    def update(self, event):
        pass


if __name__ == '__main__':
    #import cProfile
    #cProfile.run('main()')
    main()
