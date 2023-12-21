from .figura import Protagonist, Enemy, NPC
from .command import CommandDAO


class Facade:
    """
    Facade class representing the interface for interacting with game entities and data.

    Attributes:
        protagonist (Protagonist): The main character in the game.
        enemy (Enemy): The enemy character in the game.
        command_dao (CommandDAO): Data access object for retrieving game commands and information.

    Methods:
        location_id(): Get the current location ID of the protagonist.
        direction(): Get the available directions for the current location.
        name_location(): Get the name of the current location.
        description_location(): Get the description of the current location.
        story_line(line_id): Get the story line data for the specified line ID.
        change_health(line_id): Change the health, experience, and enemy health based on the specified line ID.
        check_move_next_location():Check if the protagonist can move to the next location.
    """

    def __init__(self, user_name: str):
        """
        Initialize the Facade with a user name.

        Args:
            user_name (str): The name of the user.
        """
        self.protagonist = Protagonist(user_name)
        self.enemy = Enemy(user_name)
        self.command_dao = CommandDAO()

    @property
    def location_id(self):
        """
        Get the current location ID of the protagonist.
        """
        return self.protagonist.curr_location

    @property
    def direction(self):
        """
        Get the available directions for the current location.
        """
        data = self.command_dao.get_direction(self.location_id)
        return [item[0] for item in data] if data else []

    @property
    def name_location(self):
        """
        Get the name of the current location.
        """
        return self.command_dao.get_name_location(self.location_id)

    @property
    def description_location(self):
        """
        Get the description of the current location.
        """
        return self.command_dao.get_description_location(self.location_id)

    def story_line(self, line_id):
        """
        Get the story line data for the specified line ID and update game state
        accordingly.

        Args
            line_id (int): The ID of the story line.

        Returns:
            dict or None: The story line data if available, otherwise None.
        """
        if (line_id == 51 and (self.protagonist.hp < 5 or self.protagonist.xp < 10)):
            line_id = 29
        data = self.command_dao.get_story_line(line_id)
        if line_id != self.protagonist.line_id:
            self.change_healith(line_id)
        self.protagonist.line_id = line_id
        if (data):
            data['text'] = data['text'].replace(
                "{name_surname}", self.protagonist.name)
        if (line_id in (25, 27, 29)):
            self.protagonist.curr_location = 9
        if (line_id == 20):
            self.protagonist.take("Укол")
        return data

    def change_healith(self, line_id):
        """
        Change the health, experience, and enemy health based on the specified line ID.

        Args
            line_id (int): The ID of the story line.
        """
        res = self.command_dao.change_healith(line_id)
        if res:
            self.protagonist.take_hit(-res.health)
            self.protagonist.advance_xp(res.experience)
            self.enemy.take_hit(-res.health_enemy)
        elif (line_id == 59):
            health_enemy = self.enemy.hp
            self.enemy.take_hit(health_enemy)

    def check_move_next_location(self):
        """
        Check if the protagonist can move to the next location.

        Returns:
            bool: True if the protagonist can move to the next location,
                otherwise False.
        """
        max_line_id = self.command_dao.get_max_line_id_location(
            self.location_id)
        return max_line_id >= self.location_id
