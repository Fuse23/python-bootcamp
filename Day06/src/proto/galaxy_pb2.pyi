from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GalacticCoordinates(_message.Message):
    __slots__ = ["coords"]
    COORDS_FIELD_NUMBER: _ClassVar[int]
    coords: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, coords: _Optional[_Iterable[float]] = ...) -> None: ...

class Ship(_message.Message):
    __slots__ = ["alignment", "name", "length", "ship_class", "crew_size", "armed", "officers"]
    class AlignmentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        Ally: _ClassVar[Ship.AlignmentType]
        Enemy: _ClassVar[Ship.AlignmentType]
    Ally: Ship.AlignmentType
    Enemy: Ship.AlignmentType
    class ShipType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        Corvette: _ClassVar[Ship.ShipType]
        Frigate: _ClassVar[Ship.ShipType]
        Cruiser: _ClassVar[Ship.ShipType]
        Destroyer: _ClassVar[Ship.ShipType]
        Carrier: _ClassVar[Ship.ShipType]
        Dreadnought: _ClassVar[Ship.ShipType]
    Corvette: Ship.ShipType
    Frigate: Ship.ShipType
    Cruiser: Ship.ShipType
    Destroyer: Ship.ShipType
    Carrier: Ship.ShipType
    Dreadnought: Ship.ShipType
    class Officer(_message.Message):
        __slots__ = ["first_name", "last_name", "rank"]
        FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
        LAST_NAME_FIELD_NUMBER: _ClassVar[int]
        RANK_FIELD_NUMBER: _ClassVar[int]
        first_name: str
        last_name: str
        rank: str
        def __init__(self, first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., rank: _Optional[str] = ...) -> None: ...
    ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    SHIP_CLASS_FIELD_NUMBER: _ClassVar[int]
    CREW_SIZE_FIELD_NUMBER: _ClassVar[int]
    ARMED_FIELD_NUMBER: _ClassVar[int]
    OFFICERS_FIELD_NUMBER: _ClassVar[int]
    alignment: Ship.AlignmentType
    name: str
    length: float
    ship_class: Ship.ShipType
    crew_size: int
    armed: bool
    officers: _containers.RepeatedCompositeFieldContainer[Ship.Officer]
    def __init__(self, alignment: _Optional[_Union[Ship.AlignmentType, str]] = ..., name: _Optional[str] = ..., length: _Optional[float] = ..., ship_class: _Optional[_Union[Ship.ShipType, str]] = ..., crew_size: _Optional[int] = ..., armed: bool = ..., officers: _Optional[_Iterable[_Union[Ship.Officer, _Mapping]]] = ...) -> None: ...
