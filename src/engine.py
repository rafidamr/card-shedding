from typing import List

from factory import create_cards
from interface import Interface
from schema.card import Card, Effect
from schema.deck import DiscardDeck, StockDeck
from schema.player import Action, Player


class Engine:
    current_player: Player
    timeout: float
    interface: Interface
    stock_deck: StockDeck
    discard_deck: DiscardDeck

    def __init__(self, timeout: float, card_init=4):
        self.timeout = timeout
        self.interface = Interface()
        self.current_player = Player("proguy", [])
        self.stock_deck = StockDeck(cards=create_cards())
        self.stock_deck.reshuffle()
        self.discard_deck = DiscardDeck(cards=[])
        self.current_player.init_cards(self.stock_deck, card_init)

    def run(self):
        # while True:
        self.interface.show_state(self.current_player, self.discard_deck)
        action = self.interface.select_actions()
        self.apply_action(action)
        self.interface.show_state(self.current_player, self.discard_deck)

    def apply_action(self, action: int):
        match action:
            case Action.PICK.value:
                self.current_player.pick_card(self.stock_deck)
            case Action.PLAY.value:
                card_idx = self.interface.select_card(self.current_player)
                card = self.current_player.draw(card_idx)
                self.discard_deck.receive_card(card)
                self.evaluate_effect(card)

        # TBD:
        # Decides who plays next and what can he can do

    def evaluate_effect(self, card: Card):
        if card.effect == Effect.SKIP:
            pass
        elif card.effect == Effect.REVERSE:
            pass
        elif card.effect == Effect.DRAW_TWO:
            pass
        elif card.effect == Effect.WILD:
            pass

    def skip(self):
        pass

    def reverse(self):
        pass

    def draw(self, num):
        pass
