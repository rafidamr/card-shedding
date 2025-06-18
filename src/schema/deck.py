from dataclasses import dataclass
from enum import Enum, auto
from typing import List

from schema.card import Card


class Type(Enum):
    STOCK = auto()
    DISCARD = auto()


@dataclass
class Deck:
    type: Type
    cards: List[Card] = []

    def reshuffle(self):
        pass
