from pathlib import Path

import tcod
import g

from game.keybindings import KEYBINDINGS
from game.states import InGame
from game.world_tools import world_init
from game.controller import Controller

import game.callbacks  # Initialize tcod.ecs callbacks

CONSOLE_WIDTH = 45
CONSOLE_HEIGHT = 45


THIS_DIR = Path(__file__, "..")
FONT = THIS_DIR / 'assets/Alloy_curses_12x12.png'


def main():
    g.console = tcod.console.Console(CONSOLE_WIDTH,CONSOLE_HEIGHT)
    tileset = tcod.tileset.load_tilesheet(FONT, 16, 16, tcod.tileset.CHARMAP_CP437)

    g.KEYBINDINGS = KEYBINDINGS

    world_init()

    g.state = InGame()

    with tcod.context.new(console=g.console, tileset=tileset) as g.context:
        while True:
            g.console.clear()
            g.state.on_render()
            g.context.present(g.console)

            if g.registry:
                while g.queue().front != g.player:
                    actor = g.queue().front
                    action = actor.components[Controller](actor)  # Choose an action based on the Controller component
                    action(actor)

            for event in tcod.event.wait():
                g.state.on_event(event)



if __name__ == '__main__':
    main()