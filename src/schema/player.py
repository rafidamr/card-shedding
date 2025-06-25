from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional, Self

from schema.card import Card, Color, Effect
from schema.deck import DiscardDeck, StockDeck


class Task(Enum):
    PASS = auto()
    PICK = auto()
    PLAY = auto()


class Direction(Enum):
    NEXT = auto()
    PREV = auto()


@dataclass
class Player:
    name: str
    cards: List[Card]
    tasks: List[Task]
    prev: Optional[Self]
    next: Optional[Self]

    def init_cards(self, deck: StockDeck, num: int):
        for _ in range(num):
            self.cards.append(deck.pop())

    def pick_card(self, deck: StockDeck):
        self.cards.append(deck.pop())

    def discard(self, card_idx: int, deck: DiscardDeck) -> Card:
        pcard = self.cards[card_idx]
        dcard = deck.cards[-1]
        if (
            pcard.color == dcard.color
            or pcard.number == dcard.number
            or (pcard.effect == dcard.effect and pcard.effect != Effect.NONE)
            or pcard.color == Color.WILD
        ):
            card = self.cards.pop(card_idx)
            deck.receive(card)
            return card
        raise Exception("Card is not applicable")

    def init_tasks(self):
        self.tasks = [Task.PICK, Task.PLAY]

    def has_tasks(self):
        return len(self.tasks) > 0

    def change_player(self, d: Direction) -> Optional[Self]:
        return self.next if d == Direction.NEXT else self.prev
