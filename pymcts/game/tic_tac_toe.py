from ..mc_tree import State, PlayerIdx
from copy import copy
from enum import Enum
from typing import Optional, Dict, Iterable, Hashable, Tuple


class CellState(Enum):
    EMPTY = 0
    X = 1
    O = 2

    def __str__(self):
        if self == CellState.EMPTY:
            return '.'
        else:
            return self.name


class TicTacToeState(State):
    WINNING_POSITIONS = [[(0, 0), (0, 1), (0, 2)],
                         [(1, 0), (1, 1), (1, 2)],
                         [(2, 0), (2, 1), (2, 2)],
                         [(0, 0), (1, 0), (2, 0)],
                         [(0, 1), (1, 1), (2, 1)],
                         [(0, 2), (1, 2), (2, 2)],
                         [(0, 0), (1, 1), (2, 2)],
                         [(0, 2), (1, 1), (2, 0)]]

    def __init__(self) -> None:
        self._previous_player = 2
        self._board = [[CellState.EMPTY] * 3, [CellState.EMPTY] * 3, [CellState.EMPTY] * 3]

    @property
    def result(self) -> Optional[Dict[PlayerIdx, float]]:
        # Check for win and return
        for (x1, y1), (x2, y2), (x3, y3) in self.WINNING_POSITIONS:
            if (self._board[x1][y1] in (CellState.X, CellState.O) and
                            self._board[x1][y1] == self._board[x2][y2] == self._board[x3][y3]):
                p1_result = 1.0 if self._board[x1][y1].value == 1 else 0.0
                return {1: p1_result, 2: 1.0 - p1_result}

        # Otherwise, if the board has any empty spaces, we're not yet at a terminal state
        if any(cell == CellState.EMPTY for row in self._board for cell in row):
            return None
        else:
            return {1: 0.5, 2: 0.5}

    @property
    def moves(self) -> Iterable[Hashable]:
        if not self.result:
            return [(x, y)
                    for x in range(3)  # type: ignore
                    for y in range(3)
                    if self._board[x][y] == CellState.EMPTY]
        else:
            return []

    def do_move(self, move: Tuple[int, int]) -> None:
        x, y = move
        if self._board[x][y] == CellState.EMPTY:
            self._board[x][y] = CellState(self.current_player)
            self._previous_player = self.current_player
        else:
            raise ValueError

    @property
    def previous_player(self) -> PlayerIdx:
        return self._previous_player

    @property
    def current_player(self) -> PlayerIdx:
        return 3 - self._previous_player

    def __repr__(self):
        s = ""
        for row in self._board:
            for cell in row:
                s += str(cell)
            s += '\n'
        return s
