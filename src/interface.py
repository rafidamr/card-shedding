from schema.deck import DiscardDeck
from schema.player import Action, Player


class Interface:
    def show_state(self, player: Player, dd: DiscardDeck):
        print(f"Player: {player.name}")
        print(f"Available cards:")
        for i, card in enumerate(player.cards):
            print(f"{i}. {card}")
        if len(dd.cards) > 0:
            print(f"Discard card: {dd.cards[-1]}")

    def select_actions(self) -> int:
        print("Available actions:")
        for action in list(Action):
            print(f"{action.value}. {action.name}")
        option = input("Choose your action:")
        return int(option)

    def select_card(self, player: Player) -> int:
        print("Available cards:")
        for i, card in enumerate(player.cards):
            print(f"{i}. {card}")
        option = input("Choose your card:")
        return int(option)
