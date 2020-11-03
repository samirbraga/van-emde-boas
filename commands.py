from enum import Enum, unique, auto


@unique
class Cmd(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.replace('_', ' ')

    INC = auto()
    REM = auto()
    SUC = auto()
    PRE = auto()

    def __str__(self):
        return self.value
