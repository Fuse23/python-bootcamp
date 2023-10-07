import unittest
from morality import *
from itertools import combinations

class TestGame(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game()
        self.players = [Copycat(), Cheater(), Cooperator(), Grudger(), Detective()]


    def test_copycat(self) -> None:
        self.players[0].make_move("cheat")
        self.assertEqual(self.players[0].move, "cheat")
        self.players[0].make_move("cooperate")
        self.assertEqual(self.players[0].move, "cooperate")


    def test_cheater(self) -> None:
        self.players[1].make_move()
        self.assertEqual(self.players[1].move, "cheat")


    def test_cooperator(self) -> None:
        self.players[2].make_move()
        self.assertEqual(self.players[2].move, "cooperate")


    def test_grudger(self) -> None:
        self.players[3].make_move("cooperate")
        self.assertEqual(self.players[3].move, "cooperate")
        self.players[3].make_move("cheat")
        self.assertEqual(self.players[3].move, "cheat")
        self.players[3].make_move("cooperate")
        self.assertEqual(self.players[3].move, "cheat")
        self.players[3].make_move("cooperate")
        self.assertEqual(self.players[3].move, "cheat")


    def test_detective_cheat(self) -> None:
        self.players[4].detective_move("cooperate", 0)
        self.assertEqual(self.players[4].move, "cooperate")
        self.players[4].detective_move("cooperate", 1)
        self.assertEqual(self.players[4].move, "cheat")
        self.players[4].detective_move("cooperate", 2)
        self.assertEqual(self.players[4].move, "cooperate")
        self.players[4].detective_move("cooperate", 3)
        self.assertEqual(self.players[4].move, "cooperate")
        self.players[4].detective_move("cooperate", 4)
        self.assertEqual(self.players[4].move, "cheat")
        self.players[4].detective_move("cheat", 5)
        self.assertEqual(self.players[4].move, "cheat")


    def test_detective_copycat(self) -> None:
        self.players[4].detective_move("cooperate", 0)
        self.assertEqual(self.players[4].move, "cooperate")
        self.players[4].detective_move("cooperate", 1)
        self.assertEqual(self.players[4].move, "cheat")
        self.players[4].detective_move("cheat", 2)
        self.assertEqual(self.players[4].move, "cooperate")
        self.players[4].detective_move("cooperate", 3)
        self.assertEqual(self.players[4].move, "cooperate")
        self.players[4].detective_move("cooperate", 4)
        self.assertEqual(self.players[4].move, "cooperate")
        self.players[4].detective_move("cheat", 5)
        self.assertEqual(self.players[4].move, "cheat")


    def test_results(self) -> None:
        for player1, player2 in combinations(self.players, 2):
            self.game.play(player1, player2)
        self.assertEqual(self.game.registry[str(self.players[0])], 57)
        self.assertEqual(self.game.registry[str(self.players[1])], 45)
        self.assertEqual(self.game.registry[str(self.players[2])], 29)
        self.assertEqual(self.game.registry[str(self.players[3])], 46)
        self.assertEqual(self.game.registry[str(self.players[4])], 45)


    def test_copycat_vs_cheater(self) -> None:
        copycat, cheater = self.players[0], self.players[1]
        self.game.play(copycat, cheater)
        self.assertEqual(self.game.registry[str(copycat)], -1)
        self.assertEqual(self.game.registry[str(cheater)], 3)


    def test_copycat_vs_cooperator(self) -> None:
        copycat, cooperator = self.players[0], self.players[2]
        self.game.play(copycat, cooperator)
        self.assertEqual(self.game.registry[str(copycat)], 20)
        self.assertEqual(self.game.registry[str(cooperator)], 20)


    def test_copycat_vs_grudger(self) -> None:
        copycat, grudger = self.players[0], self.players[3]
        self.game.play(copycat, grudger)
        self.assertEqual(self.game.registry[str(copycat)], 20)
        self.assertEqual(self.game.registry[str(grudger)], 20)


    def test_copycat_vs_detective(self) -> None:
        copycat, detective = self.players[0], self.players[4]
        self.game.play(copycat, detective)
        self.assertEqual(self.game.registry[str(copycat)], 18)
        self.assertEqual(self.game.registry[str(detective)], 18)


    def test_cheater_vs_cooperate(self) -> None:
        cheater, cooperator = self.players[1], self.players[2]
        self.game.play(cheater, cooperator)
        self.assertEqual(self.game.registry[str(cheater)], 30)
        self.assertEqual(self.game.registry[str(cooperator)], -10)


    def test_cheater_vs_grudger(self) -> None:
        cheater, grudger = self.players[1], self.players[3]
        self.game.play(cheater, grudger)
        self.assertEqual(self.game.registry[str(cheater)], 3)
        self.assertEqual(self.game.registry[str(grudger)], -1)


    def test_cheater_vs_detective(self) -> None:
        cheater, detective = self.players[1], self.players[4]
        self.game.play(cheater, detective)
        self.assertEqual(self.game.registry[str(cheater)], 9)
        self.assertEqual(self.game.registry[str(detective)], -3)


    def test_cooperator_vs_grudger(self) -> None:
        cooperator, grudger = self.players[2], self.players[3]
        self.game.play(cooperator, grudger)
        self.assertEqual(self.game.registry[str(cooperator)], 20)
        self.assertEqual(self.game.registry[str(grudger)], 20)


    def test_cooperator_vs_detective(self) -> None:
        cooperator, detective = self.players[2], self.players[4]
        self.game.play(cooperator, detective)
        self.assertEqual(self.game.registry[str(cooperator)], -1)
        self.assertEqual(self.game.registry[str(detective)], 27)


    def test_grudger_vs_detective(self) -> None:
        grudger, detective = self.players[3], self.players[4]
        self.game.play(grudger, detective)
        self.assertEqual(self.game.registry[str(grudger)], 7)
        self.assertEqual(self.game.registry[str(detective)], 3)


if __name__ == "__main__":
    unittest.main()
