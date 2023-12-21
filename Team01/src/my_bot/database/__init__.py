from .defaultdb import DefaultDatabase

"""
A module for managing the sqlite3 game database.

Variables:
    DATABASE (str): The path to the database file.
"""


DATABASE = "game.db"  # "database/game.db"


class UserInfo(DefaultDatabase):
    """
    Class for managing user information.

    Attributes:
        TABLE_NAME (str): Name of the table in the database.

    Methods:
        __init__(self, db_name=DATABASE): Initialize the UserInfo object and
            create the table in the database.
        insert_user_field(self, telegram_id, username, first_name, is_bot):
            Insert a user record into the table.
        get_telegram_id(self, telegram_id): Get the Telegram ID of a user from
            the table.
    """
    def __init__(self, db_name=DATABASE):
        """Create the table in the database."""
        super().__init__(db_name)
        self.table_name = "user_info"
        self.create_tables(
            self.table_name,
            "telegram_id INTEGER UNIQUE",
            "username TEXT",
            "first_name TEXT",
            "is_bot INTEGER",
            )

    def insert_field(
        self,
        telegram_id,
        username,
        first_name,
        is_bot,
    ):
        """
        Insert a user record into the table.

        Args:
            telegram_id (int): Telegram ID of the user.
            username (str): Username of the user.
            first_name (str): First name of the user.
            is_bot (int): Indicator of whether the user is a bot.
        """
        existing_telegram_id = self.get_telegram_id(telegram_id)
        if not existing_telegram_id:
            data = {
            "telegram_id": telegram_id,
            "username": username,
            "first_name": first_name,
            "is_bot": is_bot
            }
            self.insert_data(self.table_name, data)

    def get_telegram_id(self, telegram_id):
        """
        Get the Telegram ID of a user from the table.

        Args:
            telegram_id (int): Telegram ID of the user.

        Returns:
            int or None: Telegram ID if found, otherwise None.
        """
        cursor = self.connect_db.cursor()
        query = f"""
        SELECT telegram_id 
          FROM {self.table_name} 
         WHERE telegram_id = ?
        """
        cursor.execute(query, (telegram_id, ))
        result = cursor.fetchone()
        return result[0] if result else None


class UserProgress(DefaultDatabase):
    """
    Class for managing user progress in the game.

    Attributes:
        TABLE_NAME (str): Name of the table in the database.

    Methods:
        __init__(self, db_name=DATABASE): Create the table in the database.
        insert_user_progress(self, telegram_id, plot_code): Insert or update
            a user's progress in the table.
        get_plot_code(self, telegram_id): Get the plot code for a user from
            the table.
    """
    def __init__(self, db_name=DATABASE):
        """Create the table in the database"""
        super().__init__(db_name)
        self.table_name = "user_progress"
        self.create_tables(
            self.table_name,
            "telegram_id INTEGER UNIQUE",
            "plot_code INTEGER",
            )
    
    def insert_field(
        self,
        telegram_id,
        plot_code,
    ):
        """
        Insert or update a user's progress in the table.

        Args:
            telegram_id (int): Telegram ID of the user.
            plot_code (int): Code representing the user's progress in the game.
        """
        data = {
            "telegram_id": telegram_id,
            "plot_code": plot_code,
        }
        self.insert_or_replace_data(self.table_name, data)

    def get_plot_code(self, telegram_id):
        """
        Get the plot code for a user from the table.

        Args:
            telegram_id (int): Telegram ID of the user.

        Returns:
            int: Plot code for the user.
        """
        cursor = self.connect_db.cursor()
        query = f"""
        SELECT plot_code
          FROM {self.table_name} 
         WHERE telegram_id = ?
        """
        cursor.execute(query, (telegram_id, ))
        result = cursor.fetchone()
        return result[0] if result else 1


class HeroName(DefaultDatabase):
    """
    Class for managing hero names in the game.

    Attributes:
        TABLE_NAME (str): Name of the table in the database.

    Methods:
        __init__(self, db_name=DATABASE): Create the table in the database.
        insert_hero_name(self, telegram_id, hero_name): Insert or update a
            hero's name in the table.
        get_hero_name(self, telegram_id): Get the hero's name for a user from
            the table.

    """
    def __init__(self, db_name=DATABASE):
        """Create the table in the database"""
        super().__init__(db_name)
        self.table_name = "hero_name"
        self.create_tables(
            self.table_name,
            "telegram_id INTEGER UNIQUE",
            "hero_name TEXT",
            )

    def insert_field(
        self,
        telegram_id,
        hero_name,
    ):
        """
        Insert or update a hero's name in the table.

        Args:
            telegram_id (int): Telegram ID of the user.
            hero_name (str): Name of the hero.
        """
        data = {
            "telegram_id": telegram_id,
            "hero_name": hero_name,
        }
        self.insert_or_replace_data(self.table_name, data)

    def get_hero_name(self, telegram_id):
        """
        Get the hero's name for a user from the table.

        Args:
            telegram_id (int): Telegram ID of the user.

        Returns:
            str or None: Hero's name if found, otherwise None.
        """
        cursor = self.connect_db.cursor()
        query = f"""
        SELECT hero_name
          FROM {self.table_name} 
         WHERE telegram_id = ?
        """
        cursor.execute(query, (telegram_id, ))
        result = cursor.fetchone()
        return result[0] if result else None
