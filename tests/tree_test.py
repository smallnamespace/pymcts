from hypothesis import given, strategies as st
from pymcts.tree import Node

tree_value_strategy = st.floats() | st.booleans() | st.text()


@given(tree_value_strategy)
def test_value(x):
    assert Node(x).value is x


# Random nodes
node_strategy = st.builds(Node, tree_value_strategy)
# Random trees
tree_strategy = st.recursive(node_strategy,
                             lambda children: st.builds(Node, tree_value_strategy, st.lists(children)))


@given(tree_strategy)
def test_shallow_children(tree):
    for child in tree.children:
        assert child.parent is tree
