from enum import IntEnum, auto


class DeviceModel(IntEnum):
    UNKNOWN = 0
    VLP16 = auto()
    VLP32C = auto()
    

class Mode(IntEnum):
    STRONGEST = auto()
    LAST = auto()
    DUAL = auto()
    
    