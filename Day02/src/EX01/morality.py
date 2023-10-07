from collections import Counter
import itertools
from typing import Any


class Player:
    def __init__(self) -> None:
        self.move: str | None = None


    def cheat(self) -> None:
        self.move = "cheat"


    def cooperate(self) -> None:
        self.move = "cooperate"


    def reset(self) -> None:
        self.move = None


class Cheater(Player):
    def make_move(self) -> None:
        self.cheat()


    def __str__(self) -> str:
        return "cheater"


class Cooperator(Player):
    def make_move(self) -> None:
        self.cooperate()


    def __str__(self) -> str:
        return "cooperator"


class Copycat(Player):
    def make_move(self, prev_opponent_move: str | None) -> None:
        if prev_opponent_move == "cheat":
            self.cheat()
        else:
            self.cooperate()


    def __str__(self) -> str:
        return "copycat"


class Grudger(Player):
    def make_move(self, prev_opponent_move: str | None) -> None:
        if self.move == "cheat" or prev_opponent_move == "cheat":
            self.cheat()
        else:
            self.cooperate()


    def __str__(self) -> str:
        return "grudger"


class Detective(Copycat):
    def __init__(self) -> None:
        super().__init__()
        self.cheater: bool = False


    def detective_move(self, prev_opponent_move: str | None, round_number: int) -> None:
        if prev_opponent_move == "cheat":
            self.cheater = True
        if round_number < 4:
            if round_number == 1:
                self.cheat()
            else:
                self.cooperate()
        elif self.cheater:
            super().make_move(prev_opponent_move)
        else:
            self.cheat()


    def reset(self) -> None:
        super().reset()
        self.cheater = False


    def __str__(self) -> str:
        return "detective"


class MyPlayer(Copycat):
    def my_player_move(self, prev_opponent_move: str | None, is_last_round: bool) -> None:
        if not is_last_round:
            super().make_move(prev_opponent_move)
        else:
            self.cheat()

    def __str__(self):
        return "myPlayer"


class Game:
    def __init__(self, matches=10) -> None:
        self.matches: int = matches
        self.registry: Counter = Counter()


    def count(self, player1, player2) -> None:
        if player1.move == "cooperate" and player2.move == "cooperate":
            self.registry[str(player1)] += 2
            self.registry[str(player2)] += 2
        elif player1.move == "cooperate" and player2.move == "cheat":
            self.registry[str(player1)] -= 1
            self.registry[str(player2)] += 3
        elif player1.move == "cheat" and player2.move == "cooperate":
            self.registry[str(player1)] += 3
            self.registry[str(player2)] -= 1


    def player_make_move(self, player, prev_opponent_move: str, round_number: int) -> None:
        if str(player) == "detective":
            player.detective_move(prev_opponent_move, round_number)
        elif str(player) in ("copycat", "grudger"):
            player.make_move(prev_opponent_move)
        elif str(player) in ("cooperator", "cheater"):
            player.make_move()
        else:
            player.my_player_move(prev_opponent_move, round_number == self.matches-1)


    def play(self, player1, player2) -> None:
        for round in range(self.matches):
            prev_move_player1 = player1.move
            prev_move_player2 = player2.move
            self.player_make_move(player1, prev_move_player2, round)
            self.player_make_move(player2, prev_move_player1, round)
            self.count(player1, player2)
        player1.reset()
        player2.reset()


    def top3(self) -> None:
        for elem in self.registry.most_common(3):
            player, score = elem
            print(player, score)


if __name__ == "__main__":
    players: list[Player] = [Copycat(), Cheater(), Cooperator(), Grudger(), Detective()]
    game = Game()
    pairs = itertools.combinations(players, 2)
    for player1, player2 in pairs:
        game.play(player1, player2)
    game.top3()
    print()
    players.append(MyPlayer())
    new_game = Game()
    pairs = itertools.combinations(players, 2)
    for player1, player2 in pairs:
        new_game.play(player1, player2)
    new_game.top3()
