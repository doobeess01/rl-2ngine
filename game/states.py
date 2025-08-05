import tcod.camera

import g

from game.state import State
from game.action import Action, Pass
from game.tiles import TILES
from game.components import Position, Graphic, Tiles, MapShape, Name, HP, MaxHP, Quantity
from game.tags import IsItem, IsCreature
from game.message_log import MessageLog
from game.text import Text
from game.entity_tools import inventory

import game.actions as actions
import game.colors as colors


class Menu(State):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.cursor = 0
        self.options = self.get_options()

    def move_cursor(self, direction: int):
        # Don't question this, it works
        self.cursor = len(self.options)-1 if not self.cursor+direction+1 else 0 if self.cursor+direction-1 == len(self.options)-1 else self.cursor+direction

    def get_options(self) -> list[tuple[Text, Action]]:
        return []

    def select(self):
        self.options[self.cursor][1](g.player)  # Execute the action
        self.options = self.get_options()
        if self.cursor >= len(self.options):
            self.cursor = len(self.options)-1


class ItemList(Menu):
    def __init__(self, title: str, action: Action = Pass, parent=None):
        self.title = title
        self.action = action
        super().__init__(parent)
    def get_options(self) -> list[tuple[Text, Action]]:
        return [(Text(e.components[Name]+(f' (x{e.components[Quantity]})' if e.components[Quantity] > 1 else ''),fg=e.components[Graphic].fg, bg=e.components[Graphic].bg), self.action(e)) for e in self.get_items()]
    def get_items(self):
        return []
    def on_render(self):
        fg, bg = colors.DEFAULT
        g.console.print(0,0,self.title,fg=fg,bg=bg)
        for i,option in enumerate(self.options):
            option[0].print(1,2+i, invert=True if i==self.cursor else False)


class InventoryView(ItemList):
    def __init__(self, parent=None):
        super().__init__('Inventory', parent=parent)
    def get_items(self):
        return inventory(g.player)

class PickupItemsMenu(ItemList):
    def __init__(self, parent=None):
        super().__init__('Pick up which?', action=actions.PickupItem, parent=parent)
    def get_items(self):
        return [e for e in g.registry.Q.all_of(tags=[g.player.components[Position], IsItem])] 
    
class DropItemsMenu(ItemList):
    def __init__(self, parent=None):
        super().__init__('Drop which?', action=actions.DropItem, parent=parent)
    def get_items(self):
        return inventory(g.player)


class InGame(State):
    def on_render(self):
        g.console.draw_frame(-1,-1,g.CAMERA_DIMENSIONS[1]+2, g.CAMERA_DIMENSIONS[0]+2)

        map_ = g.player.components[Position].map_
        camera = tcod.camera.get_camera(g.CAMERA_DIMENSIONS, g.player.components[Position].ij)
        screen_slice, world_slice = tcod.camera.get_slices(g.CAMERA_DIMENSIONS, map_.components[MapShape], camera)
        g.console.rgb[screen_slice] = TILES['graphic'][map_.components[Tiles][world_slice]]

        rendered_priority: dict[Position, int] = {}
        for e in g.registry.Q.all_of(components=[Graphic, Position], tags=[map_]):
            pos = e.components[Position]

            render_order = 1
            if IsItem in e.tags:
                render_order = 2
            if IsCreature in e.tags:
                render_order = 3
            if g.player == e:
                render_order = 4
            if rendered_priority.get(pos, 0) >= render_order:
                continue  # Do not render over a more important entity
            rendered_priority[pos] = render_order

            rendered_pos = pos - (camera[1], camera[0])
            graphic = e.components[Graphic]

            if 0 <= rendered_pos.x < g.CAMERA_DIMENSIONS[1] and 0 <= rendered_pos.y < g.CAMERA_DIMENSIONS[0]:
                g.console.rgb[["ch", "fg"]][rendered_pos.ij] = graphic.ch, graphic.fg

        g.registry[None].components[MessageLog].render((0,32), 13)

        g.console.print(32, 1, g.player.components[Name])
        g.console.print(32, 3, f'HP: {g.player.components[HP]}/{g.player.components[MaxHP]}')
