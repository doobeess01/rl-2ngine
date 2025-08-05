from game.action import Action
from game.actions import Wait

class Controller:
    def __call__(self, actor) -> Action:
        return Wait()