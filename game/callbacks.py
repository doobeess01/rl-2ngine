from tcod.ecs import callbacks, Entity

from game.components import HP, MaxHP, Position
from game.entity_tools import kill

@callbacks.register_component_changed(component=HP)
def on_hp_change(entity: Entity, old: int | None, new: int | None):
    if new is not None:
        if new < 1:
            kill(entity)
        elif new > entity.components[MaxHP]:
            entity.components[HP] = entity.components[MaxHP]

@callbacks.register_component_changed(component=Position)
def on_position_changed(entity: Entity, old: Position | None, new: Position | None) -> None:
    '''Aesthetically pleasing means of finding entity at any given coordinate.'''
    if old == new:
        return
    if old:
        entity.tags.remove(old)
        entity.tags.remove(old.map_)
    if new:
        entity.tags.add(new)
        entity.tags.add(new.map_)