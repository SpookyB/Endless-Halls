from random import randint, choice
from dataclasses import dataclass

@dataclass
class Orb:
    color: str

@dataclass
class Rune:
    color: str

@dataclass
class Other:
    name: str

class Walker():

    messages = {
        'tele': 'On move {self.move} you step on the teleport trap.',
        'orb': 'On move {self.move} you happen across the {self.feature.color} orb.',
        'full': '\tBut you are already holding the {self.item.color} orb.',
        'grab': '\tYou pick it up.',
        'rune': 'On move {self.move} you happen across the {self.feature.color} rune.',
        'insert': '\tYou insert the matching orb.',
        'missing': '\tYou are not carrying the matching orb.',
        'victory': 'You reached the room of inscription on move {self.move}!'}

    offsets = {
        0: (0, -1),
        1: (+1, 0),
        2: (0, +1),
        3: (-1, 0)}

    def __init__(self, paths, features, logging=False):
        self.paths = paths
        self.features = features
        self.setrandomroom()
        self.setrandomdirection()
        self.move = 0
        self.runes = 0
        self.item = None
        self.victory = False
        self.logging = logging

    def log(self, message):

        if self.logging:
            print(self.messages[message].format(self=self))

    def setrandomroom(self):
        self.room = (randint(0,7), randint(0,7))

    def setrandomdirection(self):
        self.direction = (choice(tuple(self.options))+2) % 4

    @property
    def options(self):
        return self.paths[self.room[1]][self.room[0]]

    @property
    def feature(self):
        return self.features[self.room[1]][self.room[0]]
    @feature.setter
    def feature(self, value):
        self.features[self.room[1]][self.room[0]] = value

    def win(self):
        self.log('victory')
        self.victory = True

    def inspectfeature(self):
        match self.feature, self.item:
            case Other('tele'), _:
                self.log('tele')
                self.setrandomroom()
                self.setrandomdirection()
                self.inspectfeature()
            case Orb(), None:
                self.log('orb')
                self.log('grab')
                self.item = self.feature
                self.feature = None
            case Orb(), _:
                self.log('orb')
                self.log('full')
            case Rune(rcolor), Orb(ocolor) if rcolor == ocolor:
                self.log('rune')
                self.log('insert')
                self.item = None
                self.feature = None
                self.runes += 1
            case Rune(), _:
                self.log('rune')
                self.log('missing')

    def resolvemovement(self):
            self.move += 1
            offset = self.offsets[self.direction]
            self.room = (self.room[0] + offset[0], self.room[1] + offset[1])
            match self.room, self.runes:
                case ((-1|8), _) | (_, (-1|8)), 5:
                    self.win()
                case ((-1|8) as x, y), _:
                    self.room = ((x + 8) % 8, (y + 4) % 8)
                case (x, (-1|8) as y), _:
                    self.room = ((x + 4) % 8, (y + 8) % 8)

    def randomchoice(self):
        match len(self.options):
            case 1: self.direction, = tuple(self.options)
            case 2: self.direction, = tuple(self.options - {(self.direction+2) % 4})
            case 3: self.direction  = choice(tuple(self.options - {(self.direction+2) % 4}))

    def randomstep(self):
        self.inspectfeature()
        self.randomchoice()
        self.resolvemovement()

    def randomwalk(self):
        while not self.victory:
            self.randomstep()
        return self.move

testpaths = (
    ({3,0,1},   {2,3},     {0,1,2},   {0,1,2,3}, {3,0},     {2},       {0,1,2},   {2,3}),
    ({1,3},     {3,0,1},   {3,0,1},   {0,1,2,3}, {2,3},     {0,1,2},   {0,1,2,3}, {2,3,0}),
    ({1,2},     {2,3},     {1,2},     {3,0,1},   {0,1,2,3}, {3,0,1},   {2,3,0},   {0,1}),
    ({3,0,1},   {0,1,2,3}, {0,1,2,3}, {1,3},     {3,0,1},   {1,3},     {0,1,2,3}, {2,3}),
    ({1,2},     {2,3,0},   {0,1,2},   {1,3},     {1,3},     {1,2,3},   {2,3,0},   {0,1}),
    ({0,1},     {2,3,0},   {0,2},     {1,2},     {1,2,3},   {2,3,0},   {0,1,2},   {1,2,3}),
    ({2,3},     {0,1,2},   {3,0,1},   {0,1,2,3}, {0,1,2,3}, {2,3,0},   {0,1,2},   {3,0}),
    ({0,2},     {0,1},     {2,3},     {0},       {0,1,2},   {3,0},     {0,2},     {1,2}))

testfeatures = [
    [Orb('purple'),  None,           None,           None,           None,           None,           None,           None],
    [None,           None,           None,           None,           None,           Orb('yellow'),  None,           None],
    [None,           None,           Rune('yellow'), None,           None,           None,           None,           Rune('red')],
    [None,           None,           None,           None,           None,           Orb('green'),   None,           None],
    [None,           None,           Orb('red'),     None,           Rune('green'),  None,           None,           None],
    [None,           None,           Other('tele'),  Rune('purple'), None,           None,           None,           None],
    [None,           Rune('blue'),   None,           None,           None,           None,           Orb('blue'),    None],
    [None,           None,           None,           None,           None,           None,           None,           None]]

if __name__ == "__main__":
    randomwalker = Walker(testpaths, [row[:] for row in testfeatures], logging=True)
    randomwalker.randomwalk()
