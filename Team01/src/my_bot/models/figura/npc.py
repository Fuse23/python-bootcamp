class NPC:
    """A class representing a Non-Player Character (NPC).

    Attributes:
        name (str): The name of the NPC.

    Methods:
        __init__(self, name: str): Initializes an NPC instance with a given name.
        talk(self): Placeholder method for NPC dialogue or communication.
        receive(self, item: str): Receives an item from the protagonist.
    """

    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        """Get NPC name"""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set NPC name"""
        self._name = value

    def talk(self) -> None:
        """Placeholder method for NPC dialogue or communication."""
        pass

    def receive(self, item: str) -> None:
        """Get item from protagonist.

        Args:
            item (str): item which NPC receive.
        """
        print(f"{self._name} receive {item}")
