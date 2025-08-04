from tcod.ecs import Entity

import g

class Action:
    def __call__(self, actor: Entity):
        self.execute(actor)
    def execute(self, actor: Entity):
        pass

class GameAction:
    def __init__(self, cost=100):
        self.cost = cost
    def __call__(self, actor: Entity):
        self.execute(actor)
        g.queue().move_front(self.cost)