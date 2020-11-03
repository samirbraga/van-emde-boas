from typing import List, Tuple
from commands import Cmd
import numpy as np


def output_writer(track: List[Tuple[Cmd, np.int64]], output_file: str) -> None:
    result = ""
    for i, log in enumerate(track):
        if log is None:
            result += '\n'
        elif type(log) is tuple:
            if isinstance(log[0], Cmd):
                if i == 0:
                    result += "%s:%d" % log
                else:
                    result += "\n%s:%d" % log
            else:
                result += "%s %d" % log
        elif type(log) is int:
            result += "%d\n" % log

    with open(output_file, "w+") as output:
        output.write(result)
