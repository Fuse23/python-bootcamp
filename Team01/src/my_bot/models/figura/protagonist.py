from ..command import CommandDAO
from collections import defaultdict

from .npc import NPC
from .enemy import Enemy
from .location import Direction
import sys
sys.path.append("..")


class Protagonist:
    """Representing the main character (protagonist) in a text-based adventure
    game.

    Attributes:
        command_db (CommandDAO): An instance of the CommandDAO class for
            handling game commands.
        name (str): The name of the protagonist.
        hp (int): The health points (HP) of the protagonist.
        xp (int): The experience points (XP) of the protagonist.
        inventory (defaultdict): A defaultdict representing the inventory of
            the protagonist.
        curr_location (int): The current location ID of the protagonist.
        line_id (int): The current dialogue line ID of the protagonist.

    Methods:
        __init__(self, name: str): Initializes a Protagonist instance
            with the given name and default attributes.
        go(self, direction: Direction): Moves the protagonist to the next
            location based on the given direction.
        whereami(self): Returns the current location ID of the
            protagonist.
        talk_to(self, npc: NPC): Placeholder method for interacting with
            NPCs through dialogue.
        attack(self, enemy: Enemy): Placeholder method for attacking enemies.
        advance_xp(self, value: int = 1): Advances the experience points of
            the protagonist by the specified value.
        heal(self, value: int = 1): Heals the protagonist by the specified amount.
        take_hit(self, damage: int = 1): Inflicts damage to the protagonist,
            handling game over if HP drops to zero.
        take(self, item: str): Adds an item to the protagonist's inventory.
        give(self, npc: NPC, item: str): Gives an item from the protagonist's
            inventory to an NPC.
        show_inventory(self) -> List: Returns a list of items in the protagonist's
            inventory.
        use_attributes(self): Uses certain attributes (heals, advances XP,
            consumes an item) based on game logic.
    """

    def __init__(self, name: str) -> None:
        self._command_db = CommandDAO()
        self._name = name
        self._hp = 10
        self._xp = 7
        self._inventory = defaultdict(int)
        self._curr_location = 1
        self._line_id = 1

    @property
    def name(self) -> str:
        """Get protagonist name"""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set protagonist name"""
        self._name = value

    @property
    def hp(self) -> int:
        """Get protagonist health"""
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        """Set protagonist health"""
        self._hp = value

    @property
    def xp(self) -> int:
        """Get protagonist xp"""
        return self._xp

    @xp.setter
    def xp(self, value: int) -> None:
        """Set protagonist xp"""
        self._xp = value

    @property
    def inventory(self) -> defaultdict:
        """Get protagonist inventory"""
        return self._inventory

    @property
    def curr_location(self) -> int:
        """Get protagonist current location"""
        return self._curr_location

    @curr_location.setter
    def curr_location(self, value: int) -> None:
        """Set protagonist current location"""
        self._curr_location = value

    @property
    def line_id(self) -> int:
        """Get protagonist line id"""
        return self._line_id

    @line_id.setter
    def line_id(self, value: int) -> None:
        """Set protagonist line id"""
        self._line_id = value

    def go(self, direction: Direction) -> int:
        """
        Moves the protagonist to the next location based on the given direction.

        Args:
            direction (Direction): The direction in which the protagonist is moving.

        Returns:
            int: The new dialogue line ID.
        """
        self.curr_location = self._command_db.get_next_location_id(
            direction, self.curr_location)
        self.line_id = self._command_db.get_start_dialog_location(
            self.curr_location)
        if (self.line_id == 51 and self.hp < 10 and self.xp < 5):
            self.line_id = 29
        return self.line_id

    def whereami(self) -> int:
        """
        Returns the current location ID of the protagonist.

        Returns:
            int: The current location ID.
        """
        return self._curr_location

    def talk_to(self, npc: NPC) -> None:
        """Placeholder method for interacting with NPCs through dialogue.

        Args:
            npc (NPC): The NPC to interact with
        """
        pass

    # from subject
    def attack(self, enemy: Enemy) -> None:
        """Placeholder method for attacking enemies.

        Args:
            enemy (Enemy): The enemy to attack.
        """
        pass

    def advance_xp(self, value: int = 1) -> None:
        """
        Advances the experience points of the protagonist by the specified value.

        Args:
            value (int): The amount by which to advance the experience points (default is 1).
        """
        self.xp += value

    def heal(self, value: int = 1) -> None:
        """
        Heals the protagonist by the specified amount.

        Args:
            value (int): The amount by which to heal (default is 1).
        """
        self.hp += value

    def take_hit(self, damage: int = 1) -> None:
        """
        Inflicts damage to the protagonist, handling game over if HP drops to zero.

        Args:
            damage (int): The amount of damage to inflict (default is 1).
        """
        self.hp -= damage
        if self.hp <= 0:
            raise Exception("Сожалеем, но вы умерли. 💔\n\nКонец игры")

    def take(self, item: str) -> None:
        """
        Adds an item to the protagonist's inventory.

        Args:
            item (str): The item to add to the inventory.
        """
        self.inventory[item] += 1

    def give(self, npc: NPC, item: str) -> None:
        """
        Gives an item from the protagonist's inventory to an NPC.

        Args:
            npc (NPC): The NPC to give the item to.
            item (str): The item to give.
        """
        self.inventory[item] -= 1
        if self.inventory[item] == 0:
            del self.inventory[item]
        npc.receive(item)

    def show_inventory(self):
        """
        Returns a list of items in the protagonist's inventory.

        Returns:
            List[str]: The list of items in the inventory.
        """
        keys_list = list(self.inventory.keys())
        return keys_list if keys_list else []

    def use_attributes(self):
        """Uses certain attributes (heals, advances XP, consumes an item)
        based on game logic.
        """
        self.heal(2)
        self.advance_xp(2)
        del self.inventory['Укол']
