from factory import create_cards
from interface import Interface
from schema.card import Effect
from schema.deck import DiscardDeck, StockDeck
from schema.player import Action, Direction, Player, create_players


class Engine:
    current_player: Player
    interface: Interface
    stock_deck: StockDeck
    discard_deck: DiscardDeck
    direction: Direction = Direction.NEXT
    active_effect: Effect = Effect.NONE

    def __init__(self, num_players: int, init_card: int):
        self.interface = Interface()
        self.stock_deck = StockDeck(cards=create_cards())
        self.stock_deck.reshuffle()
        self.discard_deck = DiscardDeck(cards=[self.stock_deck.pop()])
        self.current_player = create_players(num_players, self.stock_deck, init_card)
        self.current_player.init_actions()
        self.direction = Direction.NEXT

    def run(self):
        while True:
            try:
                # TBD:
                # apply effect on next player
                if not self.current_player.has_actions():
                    self.change_turn()
                self.interface.show_state(self.current_player, self.discard_deck)
                action = self.interface.select_actions(self.current_player)
                self.apply_action(action)
                self.interface.show_state(self.current_player, self.discard_deck)
            except Exception as e:
                print(e)

    def change_turn(self):
        def disable_effect():
            self.active_effect = Effect.NONE

        affected_player = None
        match self.active_effect:
            case Effect.SKIP:
                affected_player = self.current_player.change_player(self.direction)  # type: ignore
                self.current_player = affected_player.change_player(self.direction)  # type: ignore
            case Effect.REVERSE:
                self.direction = (
                    Direction.PREV
                    if self.direction == Direction.NEXT
                    else Direction.NEXT
                )
                affected_player = self.current_player = self.current_player.change_player(self.direction)  # type: ignore
            case Effect.DRAW_TWO:
                affected_player = self.current_player = self.current_player.change_player(self.direction)  # type: ignore
                self.current_player.pick_card(self.stock_deck)
                self.current_player.pick_card(self.stock_deck)
            case _:
                self.current_player = self.current_player.change_player(self.direction)  # type: ignore

        if affected_player:
            self.interface.effect_message(affected_player, self.active_effect)  # type: ignore
        self.current_player.init_actions()
        disable_effect()

    def apply_action(self, action: Action):
        match action:
            case Action.PICK:
                self.current_player.pick_card(self.stock_deck)
                self.current_player.actions = [Action.PLAY, Action.PASS]
            case Action.PLAY:
                if self.play():
                    self.current_player.actions = [Action.PASS]
            case Action.PASS:
                self.current_player.actions = []

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
