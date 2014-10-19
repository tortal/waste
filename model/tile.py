# Tile classes
class Tile(object):
    def __init__(self):
        pass

    def __repr__(self):
        raise NotImplementedError


    def isBlocked(self):
        return True


class DynamicTile(Tile):
    def __init__(self):
        Tile.__init__(self)

    def activate(self):
        raise NotImplementedError


class NoneTile(Tile):
    def __repr__(self):
        return "'"


class MapEdgeTile(Tile):
    def __repr__(self):
        return 'O'


class WallTile(Tile):
    def __repr__(self):
        return '#'


class FloorTile(Tile):
    def __repr__(self):
        return ' '

    def isBlocked(self):
        return False


class DoorTile(DynamicTile):
    def __init__(self):
        self.isClosed = True

    def __repr__(self):
        return 'D'

    def activate(self):
        if self.isClosed:
            self.isClosed = False
            return False
        else:
            return True


class CorridorTile(Tile):
    pass


class EnemySpawnTile(Tile):
    def __repr__(self):
        return '!'

    def isBlocked(self):
        return False


class ChestTile(Tile):
    def __repr__(self):
        return '$'

    def isBlocked(self):
        return False


class PlayerStartTile(Tile):
    def __repr__(self):
        return 'P'

    def isBlocked(self):
        return False


class NextLevelTile(Tile):
    def __repr__(self):
        return 'N'

    def isBlocked(self):
        return False
