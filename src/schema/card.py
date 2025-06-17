from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from schema.game import Game

class Color(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    YELLOW = auto()
    WILD = auto()

class Effect(Enum):
    NONE = auto()
    SKIP = auto()
    REVERSE = auto()
    DRAW_TWO = auto()
    WILD = auto()

@dataclass(frozen=True)
class Card():
    color : Color
    number : Optional[int] = None
    effect : Effect = Effect.NONE

    def apply_effect(self, game: Game):
        if self.effect == Effect.SKIP:
            pass
        elif self.effect == Effect.REVERSE:
            pass
        elif self.effect == Effect.DRAW_TWO:
            pass
        elif self.effect == Effect.WILD:
            pass
