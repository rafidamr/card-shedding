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

    def __init__(self, timeout: float, card_init: int):
        self.timeout = timeout
        self.interface = Interface()
        self.current_player = Player("pro_guy", [], [])
        self.stock_deck = StockDeck(cards=create_cards())
        self.stock_deck.reshuffle()
        self.discard_deck = DiscardDeck(cards=[self.stock_deck.pop()])
        self.current_player.init_cards(self.stock_deck, card_init)

    def run(self):
        # while True:
        try:
            self.current_player.actions = [Action.PICK, Action.PLAY]
            self.interface.show_state(self.current_player, self.discard_deck)
            action = self.interface.select_actions(self.current_player)
            self.apply_action(action)
            self.interface.show_state(self.current_player, self.discard_deck)
        except Exception as e:
            print(e)

    def apply_action(self, action: Action):
        match action:
            case Action.PICK:
                self.current_player.pick_card(self.stock_deck)
                self.current_player.actions = [Action.PLAY, Action.PASS]
            case Action.PLAY:
                if self.play():
                    self.current_player.actions = [Action.PASS]
            case Action.PASS:
                pass

        # TBD:
        # Decides who plays next and what he can do

    def play(self) -> bool:
        try:
            card_idx = self.interface.select_card(self.current_player)
            card = self.current_player.discard(card_idx, self.discard_deck)
            self.apply_effect(card)
            return True
        except Exception as e:
            raise e

    def apply_effect(self, card: Card):
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
