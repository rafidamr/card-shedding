from typing import List
from schema.card import Card, Color, Effect


def create_cards():
    cards : List[Card] = []

    for c in [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW]:
        for n in range(1, 10):
            cards.append(Card(color=c, number=n))
        for e in [Effect.SKIP, Effect.REVERSE, Effect.DRAW_TWO]:
            cards.append(Card(color=c, effect=e))

    cards.append(Card(color=Color.WILD, effect=Effect.WILD))

    return cards