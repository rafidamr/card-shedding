from factory import create_cards


if __name__ == "__main__":
    cards = create_cards()
    print(len(cards))
    print(cards[-1])
