import sys


def decypher(message: str) -> str:
    return "".join(word[0].lower() for word in message.split())


def test() -> None:
    assert decypher(
        "The only way everyone reaches Brenda rapidly is delivering groceries explicitly"
        ) == "towerbridge"
    assert decypher(
        "Britain is Great because everyone necessitates"
        ) == "bigben"
    assert decypher(
        "Have you delivered eggplant pizza at restored keep?"
    ) == "hydepark"
    print("Well done!!!")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Wrong number of args!")
        exit(-1)
    print(decypher(sys.argv[1]))

    test()
