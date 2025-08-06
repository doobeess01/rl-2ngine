import g

from game.components import Graphic, Name, Description, ItemCategory
from game.tags import IsStackable, IsItem

import game.colors as colors

def new_item(
        category: int = None,
        name: str = 'unknown creature', 
        graphic: Graphic = None, 
        desc: str = "[No description]", 
        stackable: bool = True,
        components: dict = {}, 
        tags: set = {},
        ):

    item = g.registry.new_entity(
        components = {Name: name, Graphic: graphic, Description: desc, ItemCategory: category,}|components,
        tags = tags,
    )
    item.tags.add(IsItem)
    if stackable:
        item.tags.add(IsStackable)
    return item


POTION = new_item(
    category = 3,
    name = 'potion',
    graphic = Graphic(ord('?'), colors.LIGHT_BLUE, colors.BLACK),
    desc = 'a potion.',
)
SCROLL = new_item(
    category = 4,
    name = 'scroll',
    graphic = Graphic(ord('?'), colors.LIGHT_BLUE, colors.BLACK),
    desc = 'a scroll.',
)