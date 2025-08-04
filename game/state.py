from tcod.event import KeyDown, Quit

import g

class State:
    def on_event(self, event):
        keybindings = g.KEYBINDINGS[self.__class__]
        match event:
            case KeyDown(sym=sym) if sym in keybindings:
                keybindings[sym](g.player)  # Execute the action
            case Quit():
                raise SystemExit
    def on_render(self):
        g.console.print(0,0,f'Rendering not implemented for state {self.__class__.__name__}')