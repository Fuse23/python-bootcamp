from typing import Dict


def decorator(func):
    def wrapper(*args, **kwargs):
        print("SQUEAK")
        new_purse = func(*args, **kwargs)
        return new_purse
    return wrapper


def get_ingot_count(purse: Dict[str, int]) -> int:
    if "gold_ingots" not in purse:
        return 0
    else:
        return purse["gold_ingots"]


@decorator
def add_ingot(purse: Dict[str, int]) -> Dict[str, int]:
    ignots: int = get_ingot_count(purse) + 1
    new_purse = {"gold_ingots": ignots}
    return new_purse


@decorator
def get_ingot(purse: Dict[str, int]) -> Dict[str, int]:
    ignots: int = 0 if get_ingot_count(purse) == 0 else purse["gold_ingots"] - 1
    new_purse = {"gold_ingots": ignots}
    return new_purse


@decorator
def empty(purse: Dict[str, int]) -> Dict[str, int]:
    new_purse = {"gold_ingots": 0}
    return new_purse


if __name__ == "__main__":
    purse = {"gold_ingots": 10}
    new_purse = add_ingot(get_ingot(add_ingot(empty(purse))))
    print(purse, new_purse)
