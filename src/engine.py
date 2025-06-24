from typing import List

from factory import create_cards
from interface import Interface
from schema.card import Card, Effect
from schema.deck import DiscardDeck, StockDeck
from schema.player import Action, Player, create_players


class Engine:
    current_player: Player
    timeout: float
    interface: Interface
    stock_deck: StockDeck
    discard_deck: DiscardDeck
    active_effect: Effect = Effect.NONE

    def __init__(self, num_players: int, timeout: float, card_init: int):
        # self.timeout = timeout
        self.interface = Interface()
        self.stock_deck = StockDeck(cards=create_cards())
        self.stock_deck.reshuffle()
        self.discard_deck = DiscardDeck(cards=[self.stock_deck.pop()])
        self.current_player = create_players(num_players, self.stock_deck, card_init)

    def run(self):
        while True:
            try:
                # eval(self.apply_effect())
                # TBD:
                # assign actions on transition for the same player
                self.current_player.actions = [Action.PICK, Action.PLAY]
                self.interface.show_state(self.current_player, self.discard_deck)
                action = self.interface.select_actions(self.current_player)
                self.apply_action(action)
                self.interface.show_state(self.current_player, self.discard_deck)
            except Exception as e:
                print(e)

    def apply_effect(self) -> str:
        def disable_effect():
            self.active_effect = Effect.NONE

        match self.active_effect:
            case Effect.SKIP:
                self.interface.effect_message(self.current_player, self.active_effect)
                disable_effect()
                return "continue"
        return "None"

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
            self.active_effect = card.effect
            return True
        except Exception as e:
            raise e

    def skip(self):
        pass

    def reverse(self):
        pass

    def draw(self, num):
        pass
