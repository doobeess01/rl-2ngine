from tcod.event import KeySym as K

import g
from game.actions import *
from game.states import *


KEYBINDINGS = {
    InGame: {
        K.UP: Bump((0,-1)),
        K.N8: Bump((0,-1)),

        K.N9: Bump((1,-1)),

        K.RIGHT: Bump((1,0)),
        K.N6: Bump((1,0)),

        K.N3: Bump((1,1)),

        K.DOWN: Bump((0,1)),
        K.N2: Bump((0,1)),

        K.N1: Bump((-1,1)),

        K.LEFT: Bump((-1,0)),
        K.N4: Bump((-1,0)),

        K.N7: Bump((-1,-1)),

        K.PERIOD: Wait(),
        K.N5: Wait(),
    },
}