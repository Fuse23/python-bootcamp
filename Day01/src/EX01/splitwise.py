from typing import Dict, Tuple


def splitwise(*args: Dict[str, int]) -> Tuple[Dict[str, int], ...]:
    count_ingot: int = 0
    for purse in args:
        if "gold_ingot" in purse:
            count_ingot += purse["gold_ingot"]
    purse_1 = {"gold_ingot": count_ingot//3}
    count_ingot -= count_ingot//3
    purse_2 = {"gold_ingot": count_ingot//2}
    count_ingot -= count_ingot//2
    purse_3 = {"gold_ingot": count_ingot}
    return (purse_1, purse_2, purse_3)


def test() -> None:
    purse_1, purse_2, purse_3 = splitwise(
        {"gold_ingot": 5},
        {"gold_ingot": 5},
        {"apple": 10}
    )
    assert purse_1["gold_ingot"] \
        + purse_2["gold_ingot"] \
        + purse_3["gold_ingot"] \
            == 10
    assert max(
        purse_1["gold_ingot"],
        purse_2["gold_ingot"],
        purse_3["gold_ingot"]
    ) - min(
        purse_1["gold_ingot"],
        purse_2["gold_ingot"],
        purse_3["gold_ingot"]
    ) <= 1

    purse_1, purse_2, purse_3 = splitwise(
        {"gold_ingot": 3},
        {"gold_ingot": 2},
        {"apple": 10}
    )
    assert purse_1["gold_ingot"] \
        + purse_2["gold_ingot"] \
        + purse_3["gold_ingot"] \
            == 5
    assert max(
        purse_1["gold_ingot"],
        purse_2["gold_ingot"],
        purse_3["gold_ingot"]
    ) - min(
        purse_1["gold_ingot"],
        purse_2["gold_ingot"],
        purse_3["gold_ingot"]
    ) <= 1

    purse_1, purse_2, purse_3 = splitwise(
        {"gold_ingot": 9}
    )
    assert purse_1["gold_ingot"] \
        + purse_2["gold_ingot"] \
        + purse_3["gold_ingot"] \
            == 9
    assert max(
        purse_1["gold_ingot"],
        purse_2["gold_ingot"],
        purse_3["gold_ingot"]
    ) - min(
        purse_1["gold_ingot"],
        purse_2["gold_ingot"],
        purse_3["gold_ingot"]
    ) <= 1

    purse_1, purse_2, purse_3 = splitwise(
        {"gold_ingot": 0}
    )
    assert purse_1["gold_ingot"] \
        + purse_2["gold_ingot"] \
        + purse_3["gold_ingot"] \
            == 0
    assert max(
        purse_1["gold_ingot"],
        purse_2["gold_ingot"],
        purse_3["gold_ingot"]
    ) - min(
        purse_1["gold_ingot"],
        purse_2["gold_ingot"],
        purse_3["gold_ingot"]
    ) <= 1

    print("Tests passed!")


if __name__ == "__main__":
    print(splitwise(
        {"gold_ingot": 9},
        {"gold_ingot": 2},
        {"gold_ingot": 0},
        {"gold": 100}
    ))
    # test()
