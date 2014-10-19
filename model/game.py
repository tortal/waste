from pygame.constants import K_RIGHT, K_LEFT, K_UP, K_DOWN
from cont import debug
from gamemap import GameMapGen, PlayerStartTile
from model.tile import NextLevelTile
from tile import DoorTile
from cont.event import EventBusClient, KeyboardInputEvent, PlaySoundEvent, GameOverEvent


class GameModel(EventBusClient):
    """ Main game model
    """
    def __init__(self, eventBus, config):
        EventBusClient.__init__(self, eventBus)
        self.config = config
        gen = GameMapGen()
        self.curMap = gen.getMap()
        self.mapDict = self.curMap.gameMap

        debug.log('model map\n\t')
        debug.log(self.curMap.printMap)

        self.enemies = {}

        # THIS SUCKS, TO DELETE
        self.stepCount = 0

        for xy, tile in self.mapDict.iteritems():
            if isinstance(tile, PlayerStartTile):
                self.player = Player(xy)
                #if isinstance(tile, EnemySpawnTile):
                #    self.enemies[xy] = EnemySprite(xy)

    def _canMove(self, xy):
        try:
            tile = self.mapDict[xy]
        except KeyError:
            return False
        else:
            if isinstance(tile, DoorTile):
                return tile.activate()
            elif tile.isBlocked():
                return False
            else:
                return True

    def movePlayer(self, dxdy):
        dx, dy = dxdy
        x, y = self.player.pos
        newXY = x + dx, y + dy
        if self._canMove(newXY):
            self.player.move(newXY)

            # Play Sound (THIS SUCKS: Not correct OOP)
            event = PlaySoundEvent(self.config['GameScreen']['sound_walk_path'])
            self.eventBus.broadcast(event)
            self.stepCount += 1

            if isinstance(self.mapDict[newXY], NextLevelTile):
                self.eventBus.broadcast(GameOverEvent(self.stepCount))




    def getTile(self, xy):
        return self.mapDict[xy]

    def update(self, event):
        if isinstance(event, KeyboardInputEvent):
            x, y = self.player.pos

            dx_dy = 0,0
            if event.content == K_RIGHT:
                dx_dy = 1, 0
            elif event.content == K_LEFT:
                dx_dy = -1, 0
            elif event.content == K_UP:
                dx_dy = 0, -1
            elif event.content == K_DOWN:
                dx_dy = 0, 1

            self.movePlayer(dx_dy)
            debug.log('player pos:', self.player.pos)


class Unit:
    MAX_HP = 'MAX_HP'
    HP = 'HP'
    STR = 'STR'
    DEF = 'DEF'
    SPD = 'DEX'

    def __init__(self, xy, maxHp=10, strength=10, defense=10, speed=10):
        self.pos = xy

        self.attr = {Unit.MAX_HP: maxHp,
                     Unit.HP: maxHp,
                     Unit.STR: strength,
                     Unit.DEF: defense,
                     Unit.SPD: speed
        }

    def hit(self, dmg):
        self.attr[Unit.HP] -= dmg
        if self.attr[Unit.HP] <= 0:
            return False
        else:
            return True

    def hits(self, unit):
        pass


    def isAlive(self):
        return self.attr[Unit.HP] <= 0


class Player:
    def __init__(self, xy):
        self.hp = 20
        self.pos = xy
        self.level = 0

        self.strength = 5
        self.intelligence = 5
        self.dexterity = 5

    def hit(self, x):
        self.hp -= x
        if self.hp <= 0:
            pass

    def heal(self, x):
        self.hp += x
        if self.hp >= self._maxHp():
            self.hp = self._maxHp()

    def _maxHp(self):
        MULTIPLIER = 4
        return self.strength * MULTIPLIER

    def move(self, xy):
        self.pos = xy


class Enemy(Unit):
    def __init__(self, xy, maxHp=10, strength=10, defense=10, dexterity=10):
        Unit.__init__(self, xy, maxHp, strength, defense, dexterity)



def spawnEnemy(lvl, xy):
    MULTIPLIER = 4
    if lvl == 1:
        return Enemy(xy)
    else:
        quota = MULTIPLIER * lvl