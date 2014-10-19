#  -*- coding: utf-8 -*-
# python 2.7.5
# author: roy.nard@gmail.com
# os: win32
from cont import debug

#


class EventBus(object):
    """Connects Model-View-Controller"""

    def __init__(self):
        self.listeners = []

    def addClient(self, listener):
        self.listeners.append(listener)
        return self

    def removeClient(self, listener):
        listener.eventBus = None
        return self.listeners.remove(listener)

    def broadcast(self, event):
        if not isinstance(event, TickEvent):
            debug.log('Event', event)
        for listener in self.listeners:
            listener.update(event)


class EventBusClient:
    """All listeners/broadcasters should subclass this """

    def __init__(self, eventBus):
        """ All subclasses should implement update"""
        self.eventBus = eventBus.addClient(self)

    def update(self, event):
        raise NotImplementedError


# Event Types
class Event(object):
    """ Abstract class """
    def __init__(self, content=None):
        self.content = content

    def __repr__(self):
        return '%s :: %s' % (self.__class__.__name__, self.__dict__)


class QuitEvent(Event):
    pass


class TickEvent(Event):
    pass


class KeyboardInputEvent(Event):
    def __init__(self, userInputKey):
        Event.__init__(self, userInputKey)

class MouseInputEvent(Event):
    def __init__(self, userInputKey, pos):
        Event.__init__(self, userInputKey)
        self.pos = pos

class ShowScreenEvent(Event):
    def __init__(self, screen):
        Event.__init__(self, screen)

class PlaySoundEvent(Event):
    def __init__(self, sound):
        Event.__init__(self, sound)


class GameOverEvent(Event):
    def __init__(self, stepCount):
        Event.__init__(self, stepCount)