from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional, Self

from schema.card import Card, Color, Effect
from schema.deck import DiscardDeck, StockDeck


class Action(Enum):
    PASS = auto()
    PICK = auto()
    PLAY = auto()


@dataclass
class Player:
    name: str
    cards: List[Card]
    actions: List[Action]
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


def create_players(num_players: int, deck: StockDeck, num: int) -> Player:
    player = Player("p0", [], [], next=None, prev=None)
    player.init_cards(deck, num)
    first = player
    for i in range(1, num_players):
        player.next = Player(f"p{i}", [], [], next=None, prev=player)
        player = player.next
        player.init_cards(deck, num)
    player.next = first
    return first
