from models import Facade
import sys
sys.path.append("..")

DATABASE = ".database/game.db"


class Controller:
    """
    Singleton class responsible for controlling game interactions.

    Methods:
        __new__(cls, *args, **kwargs): Creates and returns an instance of the
            Controller class.
        __init__(self, user_name: str): Initializes an instance of the
            Controller class with a user name.
        get_direction(self): Returns directions from the current location.
        get_current_location(self): Returns the name of the current location.
        get_description_current_location(self): Returns the description of the
            current location.
        go_line_script(self, line_id: int): Moves to the next line of the script.
        get_health_protogonist(self): Shows the current health of the protagonist.
        get_exp_protogonist(self): Shows the current experience points of the
            protagonist.
        get_health_enemy(self): Shows the current health of the enemy.
        get_attributes(self): Returns a list of player attributes, or None if empty.
        can_move_next_location(self, direction): Checks if the player can move
            to the next location.
        go(self, direction): Moves the main character in the specified direction.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Creates and returns an instance of the Controller class.
        If the instance already exists, returns the existing instance.

        Args:
            cls: Controller class.
            args: Positional arguments.
            kwargs: Named arguments.

        Returns:
            Controller class instance.
        """
        if not cls._instance:
            cls._instance = super(Controller, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, user_name):
        """
        Initializes an instance of the Controller class.

        Args:
            user_name (str): User name (first name and patronymic).
        """
        self._initialized = False
        self.facade = Facade(user_name)

    def get_direction(self):
        """
        Returns directions from the current location.

        Returns:
            List of current directions.
        """
        return self.facade.direction

    def get_current_location(self):
        """
        Returns the name of the current location.

        Returns:
            str: Name of the current location.
        """
        return self.facade.name_location

    def get_description_current_location(self):
        """
        Returns the description of the current location.

        Returns:
            Description of the current location.
        """
        return self.facade.description_location

    def go_line_script(self, line_id):
        """
        Moves to the next line of the script.

        Args:
            line_id (int): Identifier of the script line.

        Returns:
            Dict or None: Returns a dictionary if the script line continues,
                or None if the end of the dialogues in the current location.
        """
        return self.facade.story_line(line_id)

    def get_health_protogonist(self):
        """
        Shows the current health of the protagonist.

        Returns:
            int: Health points of the protagonist.
        """
        return self.facade.protagonist.hp

    def get_exp_protogonist(self):
        """
        Shows the current experience points of the protagonist.

        Returns:
            int: Experience points of the protagonist.
        """
        return self.facade.protagonist.xp

    def get_health_enemy(self):
        """
        Shows the current health of the enemy.

        Returns:
            int: Health points of the enemy.
        """
        return self.facade.enemy.hp

    def get_attributes(self):
        """
        Returns a list of player attributes.

        Returns:
           List: list of player attributes.
        """
        if self.facade.protagonist.show_inventory():
            return self.facade.protagonist.show_inventory()[0]
        return None

    def use_attributes(self):
        """
        Uses player attributes.

        Calls the method for using attributes of the main character through the facade.
        """
        self.facade.protagonist.use_attributes()

    def can_move_next_location(self, direction):
        """
        Checks if the player can move to the next location.

        Args:
            direction: Movement direction.

        Returns:
           bool: True - if the player can move, False - movement is restricted.
        """
        return self.facade.check_move_next_location()

    def go(self, direction):
        """
        Moves the main character in the specified direction.

        Args:
            direction: Movement direction.

        Returns:
            Dict: similar to the go_line_script function.
        """
        return self.facade.protagonist.go(direction)
