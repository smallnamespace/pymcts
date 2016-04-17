from pymcts.mc_tree import MCTNode
from pymcts.game.trivial import TrivialState


def test_trivial():
    node = MCTNode(TrivialState())
    node.mc_round()
    assert node.wins == 1
    assert node.visits == 1

    node.mc_round()
    assert node.wins == 2
    assert node.visits == 2
