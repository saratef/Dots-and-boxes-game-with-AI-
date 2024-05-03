
from typing import NamedTuple, Literal, Tuple


class Action(NamedTuple):
    Type: Literal["row", "col"]
    Position: Tuple[int, int]
