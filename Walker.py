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

    def __init__(self, paths, features, logging=False):
        self.paths = paths
        self.features = features
        self.setrandomroom()
        self.setrandomdirection()
        self.move = 0
        self.runes = 0
        self.item = False
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
        match self.feature:
            case Other('tele'):
                self.log('tele')
                self.setrandomroom()
                self.setrandomdirection()
                self.inspectfeature()
            case Orb():
                self.log('orb')
                if self.item:
                    self.log('full')
                else:
                    self.log('grab')
                    self.item = self.feature
                    self.feature = None
            case Rune(color):
                self.log('rune')
                if self.item == Orb(color):
                    self.log('insert')
                    self.item = None
                    self.feature = None
                    self.runes += 1
                else:
                    self.log('missing')

    def resolvemovement(self):
            self.move += 1
            match self.direction:
                case 0: self.room = (self.room[0], self.room[1]-1)
                case 1: self.room = (self.room[0]+1, self.room[1])
                case 2: self.room = (self.room[0], self.room[1]+1)
                case 3: self.room = (self.room[0]-1, self.room[1])
            match self.room, self.runes:
                case (-1|8, _), 5: self.win()
                case (_, -1|8), 5: self.win()
                case (-1|8, _), _: self.room = ((self.room[0] + 8) % 8, (self.room[1] + 4) % 8)
                case (_, -1|8), _: self.room = ((self.room[0] + 4) % 8, (self.room[1] + 8) % 8)

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
