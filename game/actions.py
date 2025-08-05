import g

from game.action import Action, GameAction
from game.tiles import TILES
from game.message_log import log

from game.components import Position, Tiles, Name, HP, UnarmedAttack
from game.tags import IsCreature

import game.colors as colors


class Wait(GameAction):
    def __init__(self):
        super().__init__(100)


class Directional(GameAction):
    def __init__(self, direction: tuple[int, int], cost=100):
        super().__init__(cost)
        self.direction = direction
    def dest(self, actor):
        '''Return the result of applying the direction to the actor's position.'''
        return actor.components[Position] + self.direction
    def creature(self, actor):
        for e in g.registry.Q.all_of(tags=[self.dest(actor), IsCreature]): return e  # There should be only one creature occupying a tile


class Bump(Directional):
    def __init__(self, direction: tuple[int, int]):
        super().__init__(direction, cost=-1)
    def execute(self, actor):
        creature = self.creature(actor)
        if creature:
            Melee(creature)(actor)
        else:
            Move(self.direction)(actor)

class Move(Directional):
    def execute(self, actor):
        map_ = actor.components[Position].map_
        dest = self.dest(actor)
        if TILES['walk_cost'][map_.components[Tiles][dest.ij]] > 0:
            actor.components[Position] = dest

class Melee(Action):
    def __init__(self, target):
        self.target = target
        super().__init__(cost=100)

    def execute(self, actor):
        damage = actor.components[UnarmedAttack]
        message_color = colors.MSG_ATTACK if actor != g.player else colors.DEFAULT
        log(f'{actor.components[Name]} attacks {self.target.components[Name]} for {damage} damage!', message_color)
        self.target.components[HP] -= damage