from hypothesis import assume, find, given, strategies as st

from pymcts.tree import Node, Tree

tree_value_strategy = (st.floats() | st.booleans() | st.text()).map(
    lambda v: assume(v == v) and v)
# Random nodes
node_strategy = st.builds(Node, tree_value_strategy)
# Random trees
tree_strategy = st.recursive(
    node_strategy,
    lambda children: st.builds(Node, tree_value_strategy, st.lists(children)))


@given(tree_value_strategy)
def test_value(value):
    assert Node(value).value is value
    assert Node(5).value != 4


@given(tree_strategy)
def test_equality(tree):
    assert tree == tree
    assert Node(False) != Node(True)


def apply_tree_strategy():
    return find(tree_strategy, lambda x: True)


def test_benchmark_tree_creation(benchmark):
    benchmark(apply_tree_strategy)
