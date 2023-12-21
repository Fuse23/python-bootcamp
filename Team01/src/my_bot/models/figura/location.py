class Location:
    """A place where is protagonist be.

    Attributes:
        id (int): location id.
        name (str): location name.
        description (str): location description.
    """

    def __init__(self, _id: int, name: str, descriptoin: str) -> None:
        self._id = _id
        self._name = name
        self._description = descriptoin

    @property
    def id(self) -> int:
        """Get location id"""
        return self._id

    @property
    def name(self) -> str:
        """Get location name"""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set location name"""
        self._name = value

    @property
    def description(self) -> str:
        """Get location descriptiion"""
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """Set location description"""
        self._description = value


# для метода go
class Direction:
    """Direction from current location to another.

    Attributes:
        direction (str): orientation.
    """

    def __init__(self, direction: str) -> None:
        self._direction = direction

    @property
    def direction(self) -> str:
        """Get direction"""
        return self._direction
