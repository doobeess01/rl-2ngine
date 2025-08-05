import attrs

import g

@attrs.define
class Text:
    text: str
    fg: tuple[int,int,int]
    bg: tuple[int,int,int]

    def print(self, x: int, y: int, fg: tuple[int,int,int] = None, bg: tuple[int,int,int] = None, invert:bool=False):
        fg = self.fg if not fg else fg
        bg = self.bg if not bg else bg
        g.console.print(x,y,self.text,fg=bg if invert else fg,bg=fg if invert else bg)