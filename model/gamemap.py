#  -*- coding: utf-8 -*-
# python 2.7.5
# author: roy.nard@gmail.com
# os: win32

import random

from cont.constants import NORTH, SOUTH, WEST, EAST
from tile import FloorTile, DoorTile, WallTile, NoneTile, MapEdgeTile, EnemySpawnTile, ChestTile, NextLevelTile, PlayerStartTile

#   Exceptions


class NoSuchMapLocationException(Exception):
    pass


class AreaUnavailableException(Exception):
    pass


class GameMapGen:
    """ Class for generating a map model. Uses a simple algorithm:
        The map is created with specified a
    """
    def __init__(self, dimensionXY=(30, 30), itemCount=10, enemySpawnCount=15):
        self.xSize, self.ySize = dimensionXY
        self.gameMap = {}
        self.generateDungeon(itemCount, enemySpawnCount)
        #self.printMap()

    def generateDungeon(self, itemCount, enemySpawnCount):

        # Fill the map with "Empty tiles"
        for x in xrange(self.xSize):
            for y in xrange(self.ySize):
                self.gameMap[x, y] = NoneTile()

        self._buildMapEdges()

        # Build first room at the center of the map.
        mapCenter = (self.xSize / 2, self.ySize / 2)
        roomTiles = self._buildRoom(mapCenter, (6, 6), WEST)
        self.setTile(mapCenter, WallTile())

        # TIME TO GENERATE ZE MAP!
        # roomTiles is a list of the perimeter tiles of the first room to being with.
        while roomTiles:

            randomTile = random.choice(roomTiles.keys())
            direction = roomTiles.pop(randomTile)

            dimension = random.randint(4, 10), random.randint(4, 10)

            try:
                perimeters = self._buildRoom(randomTile, dimension, direction)
            except AreaUnavailableException:
                continue
            else:
                roomTiles.update(perimeters)

                # Raze the wall leading to the new door
                x, y = randomTile
                dx, dy = direction
                newXY = x - dx, y - dy
                self.setTile(newXY, FloorTile())


        allFloorTiles = [xy for xy, t in self.gameMap.iteritems() if isinstance(t, FloorTile)]
        random.shuffle(allFloorTiles)

        playerPos = allFloorTiles.pop()
        self.gameMap[playerPos] = PlayerStartTile()

        nextLevelPos = allFloorTiles.pop()
        self.gameMap[nextLevelPos] = NextLevelTile()

        for x in xrange(itemCount):
            chestPos = allFloorTiles.pop()
            self.gameMap[chestPos] = ChestTile()

        for x in xrange(enemySpawnCount):
            spawnPos = allFloorTiles.pop()
            self.gameMap[spawnPos] = EnemySpawnTile()


    def _buildMapEdges(self):
        """ Surrounds map with edge tiles """

        for x in xrange(self.xSize):
            self.setTile((x, 0), MapEdgeTile())
            self.setTile((x, self.ySize - 1), MapEdgeTile())

        for y in xrange(self.ySize):
            self.setTile((0, y), MapEdgeTile())
            self.setTile((self.xSize - 1, y), MapEdgeTile())

    def _getEmptyArea(self, entranceXY, dimension, direction):
        xSize, ySize = dimension
        entranceX, entranceY = entranceXY
        areaTiles = []

        # Validates if a tile is available, raises exception if not. Used for every direction
        def validateTile(x, y):
            try:
                tile = self.getTile((x, y))
            except NoSuchMapLocationException:
                raise AreaUnavailableException

            if not isinstance(tile, NoneTile):
                raise AreaUnavailableException

        # Let's iterate over the tiles that are defined by entrance location, dimension and direction
        # to see if all tiles are available.
        if direction == NORTH:
            for y in xrange(entranceY, entranceY - ySize, -1):
                for x in xrange(entranceX - xSize / 2, entranceX + (xSize + 1) / 2):
                    validateTile(x, y)
                    # Tile was available! Store to list.
                    areaTiles.append((x, y))
        elif direction == SOUTH:
            for y in xrange(entranceY, entranceY + ySize):
                for x in xrange(entranceX - xSize / 2, entranceX + (xSize + 1) / 2):
                    validateTile(x, y)
                    areaTiles.append((x, y))
        elif direction == WEST:
            for x in xrange(entranceX, entranceX - xSize, -1):
                for y in xrange(entranceY - ySize / 2, entranceY + (ySize + 1) / 2):
                    validateTile(x, y)
                    areaTiles.append((x, y))
        elif direction == EAST:
            for x in xrange(entranceX, entranceX + xSize):
                for y in xrange(entranceY - ySize / 2, entranceY + (ySize + 1) / 2):
                    validateTile(x, y)
                    areaTiles.append((x, y))

        return areaTiles

    def _buildRoom(self, entranceXY, dimension, direction, randomDimension=False):
        """ Will build a room, if there is available tiles at given offsets.
            Returns a dict of the perimeters
        """

        e = 'Room floor must be at least 2x2 excluding the surrounding walls.'
        assert dimension[0] >= 4 and dimension[1] >= 4, e


        # Check if specified area is available (not used)
        try:
            areaTiles = self._getEmptyArea(entranceXY, dimension, direction)
        except AreaUnavailableException:
            raise

        ##  If we still are here, then there is enough space to build our room! (Floor and walls) ##

        # Let's find the boundaries of the available area
        if not areaTiles:
            raise AreaUnavailableException
        xZ, yZ = zip(*areaTiles)
        xLimits = (min(xZ), max(xZ))
        yLimits = (min(yZ), max(yZ))

        # We can now iterate and set the appropriate tiles on the map.
        for xy in areaTiles:
            x, y = xy
            if x in xLimits or y in yLimits:
                self.setTile(xy, WallTile())
            else:
                self.setTile(xy, FloorTile())

        # And of course, the door.
        self.setTile(entranceXY, DoorTile())


        # Room is now complete!
        # Now create a dict of tiles that are suitable for building the next mapobject on.
        suitableTiles = {}
        topLeftX, topLeftY = min(xZ), min(yZ)
        bottomRightX, bottomRightY = max(xZ), max(yZ)

        for x in xrange(topLeftX + 1, bottomRightX):
            suitableTiles[x, topLeftY - 1] = NORTH
            suitableTiles[x, bottomRightY + 1] = SOUTH

        for y in xrange(topLeftY + 1, bottomRightY):
            suitableTiles[topLeftX - 1, y] = WEST
            suitableTiles[bottomRightX + 1, y] = EAST

        return suitableTiles

    def _buildCorridor(self, entranceXY, dimension, direction, randomDimension=False):
        pass

    def getMap(self):
        return GameMap(self.gameMap, (self.xSize, self.ySize))

    def setTile(self, xy, tile):
        try:
            self.getTile(xy)  # This will throw an exception if tile does not exist
        except NoSuchMapLocationException:
            raise
        else:
            self.gameMap[xy] = tile
            return self.gameMap[xy]

    def getTile(self, xy):
        try:
            return self.gameMap[xy]
        except KeyError:
            raise NoSuchMapLocationException()


class GameMap:
    def __init__(self, gameMap, dimension):
        self.gameMap = gameMap
        self.xSize, self.ySize = dimension

    def getTile(self, xy):
        try:
            t = self.gameMap[xy]
        except KeyError:
            raise NoSuchMapLocationException
        else:
            return t.isBlocked()

    def setTile(self, xy, tile):
        try:
            self.getTile(xy)
        except:
            raise
        self.gameMap[xy] = tile

    def printMap(self):
        from sys import stdout

        for y in range(self.ySize):
            for x in range(self.xSize):
                stdout.write(repr(self.gameMap[x, y]))
            print
        print self.gameMap


if __name__ == '__main__':
    g = GameMapGen()