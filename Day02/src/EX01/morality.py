from collections import Counter


class Player:
    def __init__(self) -> None:
        pass


class Cheater(Player):
    pass


class Cooperator(Player):
    pass


class Copycat(Player):
    pass


class Grudger(Player):
    pass


class Detective(Player):
    pass


class Game:
    def __init__(self, matches: int = 10) -> None:
        self.matches = matches
        self.registry = Counter()


    def play(self, player1: Player, player2: Player):
        pass


    def top3(self):
        pass
