import functools
from schema.card import Color, Effect
from schema.deck import DiscardDeck
from schema.player import Player, Task


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
    def select_task(self, player: Player) -> Task:
        print("Available actions:")
        for task in player.tasks:
            print(f"{task.value}. {task.name}")
        option = int(input("Choose your action: "))
        if Task(option) not in player.tasks:
            raise Exception("Action is not available")
        return Task(option)

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

    @exception_handler
    def select_color(self) -> Color:
        print("Available replacement for wild:")
        colors = list(Color)
        colors.remove(Color.WILD)
        for c in colors:
            print(f"{c.value}. {c.name}")
        option = int(input("Choose your color: "))
        if Color(option) not in colors:
            raise Exception("Color is not available")
        return Color(option)

    def show_winner(self, player: Player):
        print(f"Player {player.name} wins")
        input("press any key to exit.")

    def effect_message(self, player: Player, effect: Effect):
        print(f"[{effect.name.title()}] effect applies on {player.name}")
