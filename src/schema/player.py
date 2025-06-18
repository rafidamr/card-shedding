from typing import List

from schema.card import Card


class Player:
    id: str
    cards: List[Card]

    def __init__(self, id: str):
        self.id = id

    def inspect_discard_deck(self):
        pass

    def pick_card(self):
        pass

    def play(self):
        pass
