import tcod
import tcod.ecs

import game.state
import game.queue

from typing import Final


console: tcod.console.Console
context: tcod.context.Context

state: game.state.State

registry: tcod.ecs.Registry = None
player: tcod.ecs.Entity = None


def queue():
    try:
        return registry[None].components[game.queue.Queue]
    except KeyError:
        return
def time():
    try:
        return registry[None].components[int]
    except KeyError:
        return


KEYBINDINGS: dict[game.state.State: dict]



# Global constants

CAMERA_DIMENSIONS = (39,39)