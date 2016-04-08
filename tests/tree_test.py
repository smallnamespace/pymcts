from hypothesis import find, given, strategies as st

from pymcts.tree import Node, Tree

tree_value_strategy = st.floats() | st.booleans() | st.text()
# Random nodes
node_strategy = st.builds(Node, tree_value_strategy)
# Random trees
tree_strategy = st.recursive(
    node_strategy,
    lambda children: st.builds(Node, tree_value_strategy, st.lists(children)))


@given(tree_value_strategy)
def test_value(x):
    assert Node(x).value is x


@given(tree_strategy)
def test_parent(tree: Tree):
    for node in tree.traverse_postorder():
        for child in node.children:
            assert child.parent is node


def apply_tree_strategy():
    return find(tree_strategy, lambda x: True)


def test_tree_creation(benchmark):
    benchmark(apply_tree_strategy)
