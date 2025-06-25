from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


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
class Card:
    color: Color
    number: Optional[int] = None
    effect: Effect = Effect.NONE

    def __str__(self):
        if self.effect == Effect.NONE:
            return f"{self.color.name.title()} {self.number}"
        elif self.effect in {Effect.WILD}:
            return f"{self.effect.name.title()} ({self.color.name.title()})"
        else:
            return f"{self.color.name.title()} {self.effect.name.title()}"
