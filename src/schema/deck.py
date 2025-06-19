from dataclasses import dataclass
from random import shuffle
from typing import List

from schema.card import Card, Color


@dataclass
class Deck:
    cards: List[Card]


class StockDeck(Deck):
    def reshuffle(self):
        while True:
            shuffle(self.cards)
            if self.cards[-1].color != Color.WILD:
                break

    def pop(self) -> Card:
        return self.cards.pop()


class DiscardDeck(Deck):
    def receive(self, card: Card):
        self.cards.append(card)
