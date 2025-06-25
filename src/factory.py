from typing import List
from schema.card import Card, Color, Effect
from schema.deck import StockDeck
from schema.player import Player


def create_players(num_players: int, deck: StockDeck, num: int) -> Player:
    player = Player("p0", cards=[], tasks=[], next=None, prev=None)
    player.init_cards(deck, num)
    first = player
    for i in range(1, num_players):
        player.next = Player(f"p{i}", cards=[], tasks=[], next=None, prev=player)
        player = player.next
        player.init_cards(deck, num)
    player.next = first
    first.prev = player
    return first


def create_cards():
    cards: List[Card] = []

    for c in [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW]:
        for n in range(1, 10):
            cards.append(Card(color=c, number=n))
        for e in [Effect.SKIP, Effect.REVERSE, Effect.DRAW_TWO]:
            cards.append(Card(color=c, effect=e))

    cards.append(Card(color=Color.WILD, effect=Effect.WILD))

    return cards
