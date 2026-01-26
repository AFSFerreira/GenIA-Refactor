from langgraph.graph import END, START
from enum import StrEnum, auto

class GenIANodeName(StrEnum):
    START = START
    END = END
    RESTRUCTURING_TASK = auto()
    EXPLORING_TASK = auto()
    REFINING_TASK = auto()
    CODING_TASK = auto()


class GenIAStateStatus(StrEnum):
    STARTING = auto()
    RESTRUCTURING = auto()
    EXPLORING = auto()
    REFINING = auto()
    CODING = auto()
    FINISHED = auto()

