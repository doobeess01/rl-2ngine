import tcod
import tcod.ecs

import g

from game.components import Position, Graphic, Tiles, MapShape
from game.tags import IsIn
from game.queue import Queue
from game.procgen import generate_map


def world_init():
    g.registry = tcod.ecs.Registry()
    g.player = g.registry.new_entity(components={Position: Position(5,5), Graphic: Graphic(ord('@'), (255,255,255))})
    
    shape = (40,40)

    map_ = g.registry.new_entity(components={MapShape: shape, Tiles: generate_map(shape)})
    g.player.relation_tag[IsIn] = map_

    queue = g.registry[None].components[Queue] = Queue()
    queue.add(g.player)