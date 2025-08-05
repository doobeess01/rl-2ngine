from tcod.ecs import Entity

import g

class Action:
    def __init__(self, cost=-1):
        self.cost = cost
    def __call__(self, actor: Entity):
        self.execute(actor)
        if self.cost > -1:
            g.queue().move_front(self.cost)
    def execute(self, actor: Entity):
        pass

class GameAction(Action):
    def __init__(self, cost=100):
        super().__init__(cost)
