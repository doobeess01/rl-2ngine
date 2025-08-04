import g

from game.action import Action, GameAction
from game.tiles import TILES

from game.components import Position, Tiles
from game.tags import IsCreature, IsIn


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
    def execute(self, actor):
        Move(self.direction)(actor)

class Move(Directional):
    def execute(self, actor):
        map_ = actor.relation_tag[IsIn]
        dest = self.dest(actor)
        if TILES['walk_cost'][map_.components[Tiles][dest.ij]] > 0:
            actor.components[Position] = dest
