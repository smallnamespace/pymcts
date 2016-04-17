from pymcts.uct import UCTNode
from pymcts.game.trivial import TrivialState


def test_trivial():
    node = UCTNode(TrivialState())
    node.mc_round()
    assert node.wins == 1
    assert node.visits == 1

    node.mc_round()
    assert node.wins == 2
    assert node.visits == 2


def test_two_stage():
    win_state = TrivialState()
    loss_state = TrivialState(result={1: 0})
    root_state = TrivialState(result=None, moves={1: win_state, 2: loss_state})

    root = UCTNode(root_state)
    root.mc_round()
    root.mc_round()
    assert root.wins == 1
    assert root.visits == 2

    win_node = [child for child in root.children if child.move == root.best_move()][0]
    assert win_node.wins == 1
    assert win_node.visits == 1
