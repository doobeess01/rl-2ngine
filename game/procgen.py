import numpy as np

from game.tiles import TILE_NAMES

def generate_map(shape: tuple[int,int]):
    map_ = np.full(shape, TILE_NAMES['wall'])
    map_[1:shape[0]-1, 1:shape[1]-1] = TILE_NAMES['floor']

    return map_