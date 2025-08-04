import tcod.camera

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
        camera = tcod.camera.get_camera((39,39), g.player.components[Position].ij)
        screen_slice, world_slice = tcod.camera.get_slices((39,39), map_.components[MapShape], camera)
        g.console.rgb[screen_slice] = TILES['graphic'][map_.components[Tiles][world_slice]]

        for e in g.registry.Q.all_of(components=[Graphic]):

            pos = e.components[Position]
            rendered_pos = pos - (camera[1], camera[0])
            graphic = e.components[Graphic]
            if camera[0]-1 < rendered_pos.x < 39 and camera[1]-1 < rendered_pos.y < 39:
                g.console.rgb[["ch", "fg"]][rendered_pos.ij] = graphic.ch, graphic.fg
