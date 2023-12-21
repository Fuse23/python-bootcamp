import sqlalchemy as db
from sqlalchemy.orm import declarative_base, Session, aliased
from load_map import Connection, Locations, engine
from load_all import LineScript, Script, HealthExperienceDistribution


class CommandDAO:
    """
    A Data Access Object (DAO) class for handling database queries related
    to game commands.

    Methods:
        __new__(cls, *args, **kwargs): Singleton pattern implementation to
            ensure a single instance of the class.
        __init__(self): Initializes the CommandDAO instance and sets up the
            database connection.
        get_direction(self, location_id): Retrieves the possible directions
            from a given location.
        get_name_location(self, location_id): Retrieves the name of a location
            based on its ID.
        get_description_location(self, location_id): Retrieves the description
            of a location based on its ID.
        get_story_line(self, line_id): Retrieves the story line details for a
            given line ID.
        change_healith(self, line_id): Retrieves health and experience distribution
            information for a given line ID.
        get_next_location_id(self, direction, curr_location_id): Retrieves the next
            location ID based on the current location and direction.
        get_max_line_id_location(self, curr_location_id): Retrieves the maximum line
            ID for a given location.
        get_start_dialog_location(self, curr_location_id): Retrieves the starting
            dialogue line ID for a given location.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Singleton pattern implementation to ensure a single instance of the class.

        Returns:
            CommandDAO: The single instance of the CommandDAO class.
        """
        if not cls._instance:
            cls._instance = super(CommandDAO, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """
        Initializes the CommandDAO instance and sets up the database connection.
        """
        self._initialized = False
        if not self._initialized:
            self._initialized = True

    @property
    def session(self):
        """Get new database session"""
        return Session(bind=engine)

    def get_direction(self, location_id):
        """
        Retrieves the possible directions from a given location.

        Args:
            location_id (int): The ID of the location.

        Returns:
            list: A list of possible directions.
        """
        with self.session as session:
            return session.query(Connection.direction).filter_by(location_id=location_id).all()

    def get_name_location(self, location_id):
        """
        Retrieves the name of a location based on its ID.

        Args:
            location_id (int): The ID of the location.

        Returns:
            str: The name of the location.
        """
        with self.session as session:
            return session.query(Locations.name).filter_by(id=location_id).scalar()

    def get_description_location(self, location_id):
        """
        Retrieves the description of a location based on its ID.

        Args:
            location_id (int): The ID of the location.

        Returns:
            str: The description of the location.
        """
        with self.session as session:
            return session.query(Locations.description).filter_by(id=location_id).scalar()

    def get_story_line(self, line_id):
        """
        Retrieves the story line details for a given line ID.

        Args:
            line_id (int): The ID of the story line.

        Returns:
            dict or None: A dictionary containing story line details
                (text, options, next line IDs) or None if not found.
        """
        self.line_id = line_id
        script_option_a = aliased(Script)
        script_option_b = aliased(Script)
        with self.session as session:
            res = session.query(
                Script.text.label('text_content'),
                script_option_a.text.label('option_a_text'),
                script_option_b.text.label('option_b_text'),
                LineScript.next_dialog_option_a_id,
                LineScript.next_dialog_option_b_id
            ).join(Script, LineScript.text_id == Script.id) \
                .outerjoin(script_option_a, LineScript.option_a_id == script_option_a.id) \
                .outerjoin(script_option_b, LineScript.option_b_id == script_option_b.id) \
                .filter(LineScript.text_id == line_id) \
                .first()

        if res:
            return {
                "text": res.text_content,
                "option_a": res.option_a_text,
                "option_b": res.option_b_text,
                "next_id_dial_a": res.next_dialog_option_a_id,
                "next_id_dial_b": res.next_dialog_option_b_id
            }
        else:
            return None

    def change_healith(self, line_id):
        """
        Retrieves health and experience distribution information for a given line ID.

        Args:
            line_id (int): The ID of the story line.

        Returns:
            tuple or None: A tuple containing health, experience,
                and enemy health or None if not found.
        """
        with self.session as session:
            res = session.query(
                HealthExperienceDistribution.health,
                HealthExperienceDistribution.experience,
                HealthExperienceDistribution.health_enemy,
            ).filter_by(text_id=line_id).first()
        return res

    def get_next_location_id(self, direction, curr_location_idlocation_id):
        """
        Retrieves the next location ID based on the current location and direction.

        Args:
            direction (str): The direction in which to move.
            curr_location_id (int): The ID of the current location.

        Returns:
            int or None: The next location ID or None if not found.
        """
        with self.session as session:
            new_location_id = session.query(
                Connection.target_location_id
            ).filter_by(direction=direction
                        ).filter_by(location_id=curr_location_idlocation_id).scalar()
        return new_location_id

    def get_max_line_id_location(self, curr_location_id):
        """
        Retrieves the maximum line ID for a given location.

        Args:
            curr_location_id (int): The ID of the current location.

        Returns:
            int or None: The maximum line ID or None if not found.
        """
        with self.session as session:
            max_line_id = session.query(
                db.func.max(LineScript.text_id)
            ).filter_by(location_id=curr_location_id).scalar()
        return max_line_id

    def get_start_dialog_location(self, curr_location_id):
        """
        Retrieves the starting dialogue line ID for a given location.

        Args:
            curr_location_id (int): The ID of the current location.

        Returns:
            int or None: The starting dialogue line ID or None if not found.
        """
        with self.session as session:
            text_id = session.query(
                db.func.min(LineScript.text_id)
            ).filter_by(location_id=curr_location_id).scalar()
        return text_id
