import functools
from schema.card import Effect
from schema.deck import DiscardDeck
from schema.player import Action, Player


def exception_handler(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kargs):
        try:
            return func(self, *args, **kargs)
        except Exception as e:
            raise e

    return wrapper


class Interface:
    @exception_handler
    def show_state(self, player: Player, dd: DiscardDeck):
        print("----------------------")
        print(f"Player: {player.name}")
        print(f"Available cards:")
        for i, card in enumerate(player.cards):
            print(f"{i}. {card}")
        if len(dd.cards) > 0:
            print(f"Discard deck: {dd.cards[-1]}")

    @exception_handler
    def select_actions(self, player: Player) -> Action:
        print("Available actions:")
        for action in player.actions:
            print(f"{action.value}. {action.name}")
        option = int(input("Choose your action: "))
        if Action(option) not in player.actions:
            raise Exception("Action is not available")
        return Action(option)

    @exception_handler
    def select_card(self, player: Player) -> int:
        print("Available cards:")
        for i, card in enumerate(player.cards):
            print(f"{i}. {card}")
        print("-99. Cancel action")
        option = int(input("Choose your card: "))
        if option not in range(len(player.cards)):
            raise Exception("Action canceled")
        return int(option)

    def effect_message(self, player: Player, effect: Effect):
        print(f"[{effect.name.title()}] effect applies on {player.name}")
