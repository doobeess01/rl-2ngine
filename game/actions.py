import copy

import g

from game.action import Action, GameAction
from game.tiles import TILES
from game.message_log import log
from game.state import State
from game.entity_tools import add_to_inventory, drop
from game.states import PickupItemsMenu

from game.components import Position, Tiles, Name, HP, UnarmedAttack, Quantity
from game.tags import IsCreature, IsItem

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

class Melee(GameAction):
    def __init__(self, target):
        self.target = target
        super().__init__()

    def execute(self, actor):
        damage = actor.components[UnarmedAttack]
        message_color = colors.MSG_ATTACK if actor != g.player else colors.DEFAULT
        log(f'{actor.components[Name]} attacks {self.target.components[Name]} for {damage} damage!', message_color)
        self.target.components[HP] -= damage


class PickupItem(GameAction):
    def __init__(self, item):
        self.item = item
        super().__init__()
    
    def execute(self, actor):
        log(f'{actor.components[Name]} picks up the {self.item.components[Name]}{f" (x{self.item.components[Quantity]})" if self.item.components[Quantity] > 1 else ""}.')
        add_to_inventory(self.item, actor)


class DropItem(GameAction):
    def __init__(self, item):
        self.item = item
        super().__init__()
    def execute(self, actor):
        log(f'{actor.components[Name]} drops the {self.item.components[Name]}.')
        drop(self.item)


class PickupItems(GameAction):
    def execute(self, actor):
        assert actor == g.player
        items = [e for e in g.registry.Q.all_of(tags=[actor.components[Position], IsItem])]

        if len(items) > 1:
            EnterSubstate(PickupItemsMenu)(actor)
        elif items:
            PickupItem(items[0])(actor)
        else:
            log("There's nothing to pick up here.", colors.MSG_FAILED_ACTION)


# STATE ACTIONS

class StateAction(Action):
    def __init__(self, state: State):
        self.state = state
        super().__init__()

class ChangeState(StateAction):
    def execute(self, actor):
        self.state
        g.state = self.state

class ExitState(Action):
    def execute(self, actor):
        g.state.exit()

class EnterSubstate(StateAction):
    def execute(self, actor):
        parent = g.state
        g.state = self.state(parent=parent)


class MoveCursor(Action):
    def __init__(self, step: int):
        self.step = step
        super().__init__()
    def execute(self, actor):
        g.state.move_cursor(self.step)

class Select(Action):
    def execute(self, actor):
        g.state.select()