import g

from game.components import Graphic, Name, Description
from game.tags import IsStackable

import game.colors as colors

def new_item(
        name: str = 'unknown creature', 
        graphic: Graphic = None, 
        desc: str = "[No description]", 
        stackable: bool = True,
        components: dict = {}, 
        tags: set = {},
        ):
    item = g.registry.new_entity(
        components = {Name: name, Graphic: graphic, Description: desc,}|components,
        tags = tags
    )
    if stackable:
        item.tags.add(IsStackable)
    return item


THINGY = new_item(
    name = 'thingy',
    graphic = Graphic(ord('?'), colors.LIGHT_BLUE, colors.BLACK),
    desc = 'what even is this?',
)
THINGY2 = new_item(
    name = 'thingy2',
    graphic = Graphic(ord('?'), colors.LIGHT_BLUE, colors.BLACK),
    desc = 'what even is this? again?',
)