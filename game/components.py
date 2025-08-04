import attrs
import tcod
import numpy as np
from typing import Final

@attrs.define
class Position:
    x: int
    y: int
    map_: tcod.ecs.Entity

    @property
    def ij(self):
        return self.y, self.x

    def __add__(self, other: tuple[int, int]):
        return self.__class__(self.x+other[0], self.y+other[1], self.map_)

    def __sub__(self, other: tuple[int, int]):
        return self.__class__(self.x-other[0], self.y-other[1], self.map_)

    def __hash__(self):
        return hash((self.x, self.y))

    def __iter__(self):
        return (self.x, self.y)


@attrs.define
class Graphic:
    ch: int
    fg: tuple[int, int, int]
    bg: tuple[int, int, int] = (0,0,0)


Tiles: Final = ('Tiles', np.ndarray)
MapShape: Final = ('MapShape', tuple[int, int])