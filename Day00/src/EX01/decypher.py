import sys
import argparse


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
    parser = argparse.ArgumentParser()
    parser.add_argument("message", help="Decypher the string you use here", type=str)
    args = parser.parse_args()
    print(decypher(args.message))

    # test()
