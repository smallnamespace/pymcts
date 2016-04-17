from ..mc_tree import State, PlayerIdx
from typing import Optional, Dict, Iterable, Hashable


class TrivialState(State):
    """A trivial game where Player 1 always immediately wins."""
    def __init__(self,
                 result: Optional[Dict[PlayerIdx, float]]={1: 1.0},
                 previous_player: PlayerIdx=1,
                 moves: Dict[Hashable, State]=None):
        self._result = result
        self._previous_player = previous_player
        self._moves = {}
        if moves:
            self._moves = moves

    @property
    def result(self) -> Optional[Dict[PlayerIdx, float]]:
        return self._result

    @property
    def moves(self) -> Iterable[Hashable]:
        return self._moves.keys()

    def do_move(self, move) -> 'State':
        return self._moves[move]

    @property
    def previous_player(self) -> PlayerIdx:
        return self._previous_player
