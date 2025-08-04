import tcod
import tcod.ecs

import g

from game.components import Position, Graphic, Tiles, MapShape
from game.tags import IsActor
from game.queue import Queue
from game.procgen import generate_map


def world_init():
    g.registry = tcod.ecs.Registry()
    
    shape = (40,40)
    map_ = g.registry.new_entity(components={MapShape: shape, Tiles: generate_map(shape)})
    
    g.player = g.registry.new_entity(components={Position: Position(5,5, map_), Graphic: Graphic(ord('@'), (255,255,255))})
    
    queue = g.registry[None].components[Queue] = Queue()

    enter_level(map_)


def enter_level(map_: tcod.ecs.Entity):
    g.queue().clear()
    for e in [e for e in g.registry.Q.all_of(tags=[IsActor]) if e.components[Position].map_ == map_ and e != g.player]:
        g.queue().add(e)
    g.queue().add(g.player)  # Every other entity gets a turn before the player does