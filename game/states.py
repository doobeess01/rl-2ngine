import tcod.camera

import g

from game.state import State
from game.action import Action, Pass
from game.tiles import TILES
from game.components import Position, Graphic, Tiles, MapShape, Name, HP, MaxHP, Quantity, ItemCategory, ITEM_CATEGORIES
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
        self.items = []
        super().__init__(parent)
    def get_options(self) -> list[tuple[Text, Action]]:
        options = []
        items = self.get_items()
        sorted_items = {}
        # Sort items by category
        for item in items:
            category = item.components[ItemCategory]
            if sorted_items.get(category, 0):
                sorted_items[category].append(item)
            else:
                sorted_items[category] = [item]
        # Add options
        for i in range(max(sorted_items)):
            if sorted_items.get(i+1, 0):
                for item in sorted_items[i+1]:
                    name = item.components[Name]
                    quantity = item.components[Quantity]
                    graphic = item.components[Graphic]
                    options.append((
                        Text(name+(f' (x{quantity})' if quantity > 1 else ''), graphic.fg, graphic.bg),
                        self.action(item)
                    ))
                    self.items.append(item)
        return options
    def get_items(self):
        return []
    def on_render(self):
        fg, bg = colors.DEFAULT
        g.console.print(0,0,self.title,fg=fg,bg=bg)
        line_counter = 1
        for i,option in enumerate(self.options):
            item = self.items[i]
            previous_item = self.items[i-1]
            category = item.components[ItemCategory]
            previous_category = previous_item.components[ItemCategory]
            if category != previous_category or i==0:
                line_counter += 1
                g.console.print(0,line_counter,f'-- {ITEM_CATEGORIES[category]} --')
                line_counter += 2

            option[0].print(1,line_counter, invert=True if i==self.cursor else False)
            line_counter += 1


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
