from hypothesis import given, strategies as st
from pymcts.tree import Node, Tree

tree_value_strategy = st.floats() | st.booleans() | st.text()
# Random nodes
node_strategy = st.builds(Node, tree_value_strategy)
# Random trees
tree_strategy = st.recursive(
    node_strategy,
    lambda children: st.builds(Node, tree_value_strategy, st.lists(children)))


def tree_dfs_postorder(node: Node) -> Node:
    for child in node.children:
        yield from tree_dfs_postorder(child)
    yield node


@given(tree_value_strategy)
def test_value(x):
    assert Node(x).value is x


@given(tree_strategy)
def test_parent(tree: Tree):
    for node in tree_dfs_postorder(tree):
        for child in node.children:
            assert child.parent is node
