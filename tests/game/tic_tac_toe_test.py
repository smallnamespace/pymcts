from pymcts.game.tic_tac_toe import TicTacToeState
from textwrap import dedent

import pytest


def test_tic_tac_toe():
    state = TicTacToeState()
    assert len(state.moves) == 9

    state.do_move((1, 1))
    assert state.current_player == 2
    assert len(state.moves) == 8
    assert repr(state) == dedent('''
        ...
        .X.
        ...
        ''')[1:]

    # Try an illegal move
    with pytest.raises(ValueError):
        state.do_move((1, 1))

    state.do_move((0, 0))
    state.do_move((0, 1))
    state.do_move((1, 0))
    assert not state.result

    state.do_move((2, 1))

    assert not state.moves
    # P1 win
    assert state.result == {1: 1.0, 2: 0.0}
    assert repr(state) == dedent('''
        OX.
        OX.
        .X.
        ''')[1:]
