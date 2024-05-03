from typing import NamedTuple
from numpy import ndarray


class State(NamedTuple):
    boardStatus: ndarray
    rowStatus: ndarray
    colStatus: ndarray
    player1Turn: bool
