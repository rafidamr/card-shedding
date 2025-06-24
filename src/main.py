from engine import Engine


if __name__ == "__main__":
    engine = Engine(num_players=3, timeout=0, card_init=4)
    engine.run()
