from enum import Enum, auto

class Result(Enum):
    NOTHING_MOVED = auto()
    LOSS = auto()
    KEEP_GOING = auto()
