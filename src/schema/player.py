from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional, Self

from schema.card import Card
from schema.deck import StockDeck


class Action(Enum):
    PICK = auto()
    PLAY = auto()


@dataclass
class Player:
    name: str
    cards: List[Card]

    def init_cards(self, deck: StockDeck, num: int):
        for _ in range(num):
            self.cards.append(deck.pop_card())

    def pick_card(self, deck: StockDeck):
        self.cards.append(deck.pop_card())

    def draw(self, card_idx: int):
        return self.cards.pop(card_idx)
