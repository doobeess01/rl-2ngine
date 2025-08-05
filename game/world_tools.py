import tcod
import tcod.ecs

import g

from game.components import Position, Graphic, Tiles, MapShape
from game.tags import IsActor
from game.queue import Queue
from game.procgen import generate_map
from game.entity_tools import spawn_creature, spawn_item, add_to_inventory
from game.message_log import MessageLog


def world_init():
    g.registry = tcod.ecs.Registry()

    from game.templates.creatures import PLAYER, MONSTER
    from game.templates.items import THINGY, THINGY2
    
    shape = (60,60)
    map_ = g.registry.new_entity(components={MapShape: shape, Tiles: generate_map(shape)})
    
    g.player = spawn_creature(PLAYER, Position(3,3, map_))

    g.registry[None].components[Queue] = Queue()
    g.registry[None].components[MessageLog] = MessageLog()

    monster = spawn_creature(MONSTER, Position(25,25, map_))

    add_to_inventory(spawn_item(THINGY), g.player)
    add_to_inventory(spawn_item(THINGY), g.player)
    spawn_item(THINGY, Position(1,1,map_))
    add_to_inventory(spawn_item(THINGY2), g.player)

    enter_level(map_)


def enter_level(map_: tcod.ecs.Entity):
    g.queue().clear()
    g.queue().add(g.player)
    for e in [e for e in g.registry.Q.all_of(tags=[IsActor, g.player.components[Position].map_]) if e != g.player]:
        g.queue().add(e)
