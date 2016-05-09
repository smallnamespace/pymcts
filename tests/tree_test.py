from hypothesis import assume, find, given, strategies as st

from pymcts.tree import Node, Traversal
from textwrap import dedent

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


@given(tree_strategy)
def test_traverse(tree):
    # Both traversals result in the same set of nodes
    assert (set(map(id, tree.traverse(Traversal.preorder))) ==
            set(map(id, tree.traverse(Traversal.postorder))))

    assert next(tree.traverse(Traversal.preorder)) == tree

    # Check that parent pointers are correct
    assert all(not parent or child in parent.children
               for parent, child in tree.traverse(Traversal.preorder, return_tuples=True))


def test_repr():
    tree = Node(5, [
        Node(4, [
            Node('Foo')
        ]),
        Node(3, [
            Node('Bar'),
            Node('Baz')
        ])
    ])
    expected_repr = dedent('''
        Node(5, [
            Node(4, [
                Node('Foo')
            ]),
            Node(3, [
                Node('Bar'),
                Node('Baz')
            ])
        ])''')[1:]

    assert repr(tree) == expected_repr
