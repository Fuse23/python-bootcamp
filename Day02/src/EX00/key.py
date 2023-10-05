class Key:
    # key.passphrase == "zax2rulez"
    def __init__(self) -> None:
        self.passphrase: str = "zax2rulez"


    # str(key) == "GeneralTsoKeycard"
    def __str__(self) -> str:
        return "GeneralTsoKeycard"


    # len(key) == 1337
    def __len__(self) -> int:
        return 1337


    # key > 9000
    def __gt__(self, other: int) -> bool:
        return 9001 > other


    # key[404] == 3
    def __getitem__(self, key: int) -> int:
        return 3 if key == 404 else 0
