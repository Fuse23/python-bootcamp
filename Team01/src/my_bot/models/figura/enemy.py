from .npc import NPC


class Enemy(NPC):
    """A class representing an Enemy, inheriting from the NPC (Non-Player Character)
    class.

    Attributes:
        name (str): The name of the enemy.
        _hp (int): The health points (HP) of the enemy.

    Methods:
        __init__(self, name: str): Initializes an Enemy instance with a
            given name and sets initial HP to 1.
        attack(self): Placeholder method for enemy attacks.
        take_hit(self, damage: int): Reduces the enemy's health points by
            the given damage.
    """

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._hp = 1

    @property
    def hp(self) -> int:
        """Get the current health points of the enemy."""
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        """Set the health points of the enemy."""
        self._hp = value

    def attack(self) -> None:
        """Placeholder method for enemy attacks."""
        pass

    def take_hit(self, damage: int) -> None:
        """
        Reduces the enemy's health points by the given damage.

        Raises:
            If the health points fall to or below zero, raises an exception
            indicating game over.
        """
        self._hp -= damage
        if self._hp <= 0:
            raise Exception(
                " Сожалеем, но ваш пациент не выжил. 💔😢\n\nКонец игры")
