from typing import Dict


def get_ingot_count(purse: Dict[str, int]) -> int:
    if "gold_ingots" not in purse:
        return 0
    else:
        return purse["gold_ingots"]


def add_ingot(purse: Dict[str, int]) -> Dict[str, int]:
    ignots: int = get_ingot_count(purse) + 1
    new_purse = {"gold_ingots": ignots}
    return new_purse


def get_ingot(purse: Dict[str, int]) -> Dict[str, int]:
    ignots: int = 0 if get_ingot_count(purse) == 0 else purse["gold_ingots"] - 1
    new_purse = {"gold_ingots": ignots}
    return new_purse


def empty(purse: Dict[str, int]) -> Dict[str, int]:
    new_purse = {"gold_ingots": 0}
    return new_purse


def test() -> None:
    # test for empty()
    assert empty({}) == {"gold_ingots": 0}
    assert empty({"gold_ingots": 0}) == {"gold_ingots": 0}
    assert empty({"gold_ingots": 1}) == {"gold_ingots": 0}
    assert empty({"gold": 10}) == {"gold_ingots": 0}
    # tests for add_ingot()
    assert add_ingot({}) == {"gold_ingots": 1}
    assert add_ingot({"gold_ingots": 0}) == {"gold_ingots": 1}
    assert add_ingot({"gold_ingots": 20}) == {"gold_ingots": 21}
    assert add_ingot({"gold": 20}) == {"gold_ingots": 1}
    # tests for get_ingot()
    assert get_ingot({}) == {"gold_ingots": 0}
    assert get_ingot({"gold_ingots": 0}) == {"gold_ingots": 0}
    assert get_ingot({"gold_ingots": 1}) == {"gold_ingots": 0}
    assert get_ingot({"gold_ingots": 10}) == {"gold_ingots": 9}
    assert get_ingot({"gold": 10}) == {"gold_ingots": 0}
    # tests for all
    assert add_ingot(get_ingot(add_ingot(empty(
        {"gold_ingots": 1})))) == {"gold_ingots": 1}
    assert get_ingot(add_ingot(get_ingot(add_ingot(empty(
        {}))))) == {"gold_ingots": 0}
    print("Tests passed!")


if __name__ == "__main__":
    print(add_ingot(get_ingot(add_ingot(empty({})))))
    # test()

