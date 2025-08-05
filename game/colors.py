WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (200,200,200)

RED = (255,0,0)
LIGHT_RED = (255,75,75)

GREEN = (0,255,0)
LIGHT_GREEN = (100,255,100)

BLUE = (0,0,255)
LIGHT_BLUE = (100,100,255)

DEFAULT = (WHITE, BLACK)
MSG_ATTACK = (LIGHT_RED, BLACK)
MSG_DEATH = (BLACK, LIGHT_RED)
MSG_FAILED_ACTION = (GRAY, BLACK)

def invert(colors: tuple[tuple[int,int,int], tuple[int,int,int]]):
    return colors[1], colors[0]