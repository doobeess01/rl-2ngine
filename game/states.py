import tcod.camera

import g

from game.state import State
from game.action import Action
from game.tiles import TILES

from game.components import Position, Graphic, Tiles, MapShape, Name, HP, MaxHP
from game.message_log import MessageLog


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
        g.console.draw_frame(-1,-1,g.CAMERA_DIMENSIONS[1]+2, g.CAMERA_DIMENSIONS[0]+2)

        map_ = g.player.components[Position].map_
        camera = tcod.camera.get_camera(g.CAMERA_DIMENSIONS, g.player.components[Position].ij)
        screen_slice, world_slice = tcod.camera.get_slices(g.CAMERA_DIMENSIONS, map_.components[MapShape], camera)
        g.console.rgb[screen_slice] = TILES['graphic'][map_.components[Tiles][world_slice]]

        for e in g.registry.Q.all_of(components=[Graphic, Position], tags=[map_]):
            pos = e.components[Position]
            rendered_pos = pos - (camera[1], camera[0])
            graphic = e.components[Graphic]
            if 0 <= rendered_pos.x < g.CAMERA_DIMENSIONS[1] and 0 <= rendered_pos.y < g.CAMERA_DIMENSIONS[0]:
                g.console.rgb[["ch", "fg"]][rendered_pos.ij] = graphic.ch, graphic.fg

        g.registry[None].components[MessageLog].render((0,32), 8)

        g.console.print(32, 1, g.player.components[Name])
        g.console.print(32, 3, f'HP: {g.player.components[HP]}/{g.player.components[MaxHP]}')
