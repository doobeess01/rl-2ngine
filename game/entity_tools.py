from tcod.ecs import Entity

import g

from game.components import Position, Name
from game.tags import IsCreature, IsActor

from game.message_log import log
import game.colors as colors

# Generic functions

def spawn_entity(template: Entity, position: Position, components: dict = {}, tags: set = {}) -> Entity:
    entity = template.instantiate()
    entity.components |= {Position: position}|components
    entity.tags |= tags

    return entity


# Creature functions

def spawn_creature(template: Entity, position: Position, components: dict = {}, tags: set = {}) -> Entity:
    creature = spawn_entity(template, position, components=components, tags=tags)
    creature.tags.add(IsCreature)
    creature.tags.add(IsActor)
    return creature

def kill(actor: Entity):
    g.queue().remove(actor)
    log(f'{actor.components[Name]} dies!', colors.MSG_DEATH)
    actor.clear()