from factory import create_players, create_cards
from interface import Interface
from schema.card import Effect
from schema.deck import DiscardDeck, StockDeck
from schema.player import Task, Direction, Player


class Game:
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
        self.current_player.init_tasks()

    def run(self):
        while True:
            try:
                if not self.current_player.has_tasks():
                    self.change_turn()
                self.interface.show_state(self.current_player, self.discard_deck)
                task = self.interface.select_tasks(self.current_player)
                self.perform(task)
                self.interface.show_state(self.current_player, self.discard_deck)
            except Exception as e:
                print(e)

    def perform(self, task: Task):
        match task:
            case Task.PICK:
                self.current_player.pick_card(self.stock_deck)
                self.current_player.tasks = [Task.PLAY, Task.PASS]
            case Task.PLAY:
                if self.play():
                    self.current_player.tasks = [Task.PASS]
            case Task.PASS:
                self.current_player.tasks = []

    def play(self) -> bool:
        try:
            card_idx = self.interface.select_card(self.current_player)
            card = self.current_player.discard(card_idx, self.discard_deck)
            self.active_effect = card.effect
            return True
        except Exception as e:
            raise e

    def change_turn(self):
        affected_player = None

        match self.active_effect:
            case Effect.SKIP:
                affected_player = self.skip()
            case Effect.REVERSE:
                affected_player = self.reverse()
            case Effect.DRAW_TWO:
                affected_player = self.force_draw(card_num=2)
            case Effect.WILD:
                pass
            case _:
                self.current_player = self.current_player.change_player(self.direction)  # type: ignore

        if affected_player:
            self.interface.effect_message(affected_player, self.active_effect)  # type: ignore
        self.current_player.init_tasks()
        self.active_effect = Effect.NONE

    def skip(self):
        affected_player = self.current_player.change_player(self.direction)  # type: ignore
        self.current_player = affected_player.change_player(self.direction)  # type: ignore
        return affected_player

    def reverse(self):
        self.direction = (
            Direction.PREV if self.direction == Direction.NEXT else Direction.NEXT
        )
        affected_player = self.current_player = self.current_player.change_player(self.direction)  # type: ignore
        return affected_player

    def force_draw(self, card_num: int):
        affected_player = self.current_player = self.current_player.change_player(self.direction)  # type: ignore
        for _ in range(card_num):
            self.current_player.pick_card(self.stock_deck)
        return affected_player
