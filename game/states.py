import g

from game.state import State
from game.action import Action
from game.tiles import TILES

from game.components import Position, Graphic, Tiles, MapShape
from game.tags import IsIn


'''
class Menu(State):
    def __init__(self, options: dict[str: Action]):
        super().__init__()
        self.options = options

    def move_cursor(self, direction: int):
        self.cursor = max(self.cursor + direction if self.cursor != len(self.options)-1 else 0, len(self.options)-1)
'''  # TODO: Implement


class InGame(State):
    def on_render(self):
        map_ = g.player.relation_tag[IsIn]
        g.console.rgb[0:map_.components[MapShape][0], 0:map_.components[MapShape][1]] = TILES['graphic'][map_.components[Tiles]]

        for e in g.registry.Q.all_of(components=[Graphic]):

            pos = e.components[Position]
            graphic = e.components[Graphic]
            g.console.rgb[["ch", "fg"]][pos.ij] = graphic.ch, graphic.fg
