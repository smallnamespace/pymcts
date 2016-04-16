from ..mc_tree import State, PlayerIdx
from typing import Optional, Dict, Iterable, Hashable


class TrivialState(State):
    """A trivial game where Player 1 always immediately wins."""
    @property
    def result(self) -> Optional[Dict[PlayerIdx, float]]:
        return {1: 1.0}

    @property
    def moves(self) -> Iterable[Hashable]:
        return []

    def do_move(self, move) -> 'State':
        # We shouldn't reach this state
        raise ValueError

    @property
    def previous_player(self) -> PlayerIdx:
        return 1
