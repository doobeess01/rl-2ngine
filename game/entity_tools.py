from tcod.ecs import Entity

from game.components import Position
from game.tags import IsCreature, IsActor


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