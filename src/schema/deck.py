from dataclasses import dataclass
from random import shuffle
from typing import List

from schema.card import Card


@dataclass
class Deck:
    cards: List[Card]


class StockDeck(Deck):
    def reshuffle(self):
        shuffle(self.cards)

    def pop_card(self) -> Card:
        return self.cards.pop()


class DiscardDeck(Deck):
    def receive_card(self, card: Card):
        self.cards.append(card)
