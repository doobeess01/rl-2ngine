import tcod
import tcod.ecs

import g

from game.components import Position, Graphic, Tiles, MapShape
from game.tags import IsActor
from game.queue import Queue
from game.procgen import generate_map
from game.entity_tools import spawn_creature


def world_init():
    g.registry = tcod.ecs.Registry()

    from game.templates.creatures import PLAYER, MONSTER
    
    shape = (60,60)
    map_ = g.registry.new_entity(components={MapShape: shape, Tiles: generate_map(shape)})
    
    g.player = spawn_creature(PLAYER, Position(3,3, map_))

    queue = g.registry[None].components[Queue] = Queue()

    monster = spawn_creature(MONSTER, Position(25,25, map_))
    enter_level(map_)


def enter_level(map_: tcod.ecs.Entity):
    g.queue().clear()
    g.queue().add(g.player)
    for e in [e for e in g.registry.Q.all_of(tags=[IsActor, g.player.components[Position].map_]) if e != g.player]:
        g.queue().add(e)
