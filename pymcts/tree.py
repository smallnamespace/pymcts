from enum import Enum
from typing import cast, Any, Generator, Generic, Iterable, List, Optional, TypeVar

# TODO: Add upper bound once it's supported at https://github.com/python/mypy/issues/689
N = TypeVar('N')
V = TypeVar('V', covariant=True)


class Traversal(Enum):
    preorder = 1
    postorder = 2


class Node(Generic[N, V]):
    """
    A generic tree node. Nodes point to their parents, and nodes may have multiple children.
    """
    def __init__(self, value: V, children: Iterable['N']=None) -> None:  # type: ignore
        self._children = []  # type: List[N]
        self.value = value
        if children:
            self.children = children

    @property
    def children(self) -> List['N']:
        return self._children

    @children.setter
    def children(self, children: Iterable['N']=None) -> None:
        if children:
            self._children = list(children)

    def __repr__(self):
        return self.repr()

    def repr(self, level=0) -> str:
        indent = ' ' * 4 * level
        return '{indent}{clz}({node_repr}{children})'.format(
            indent=indent,
            clz=self.__class__.__name__,
            node_repr=self.node_repr(indent),
            children=(', [\n' +
                      ',\n'.join(cast(Node, c).repr(level + 1) for c in self._children) + '\n' +
                      indent + ']') if self._children else '')

    def node_repr(self, indent: str) -> str:
        """String representation of the node's members, not including children."""
        return repr(self.value)

    def __eq__(self, other):
        """
        TODO: Is it reasonable to ignore the generic type variable?
        E.g. should Node(2.0) == Node(2) ? Currently this is True
        """
        return (isinstance(other, type(self)) and
                self.value == other.value and
                self.children == other.children)

    def traverse(self, order=Traversal.preorder) -> Generator['N', Any, 'N']:
        """
        Traverse tree rooted at this node via post-order DFS. Results are undefined if
        the tree is modified concurrently.
        """
        if order == Traversal.preorder:
            yield cast('N', self)

        for child in self.children:
            yield from cast('Node', child).traverse(order)

        if order == Traversal.postorder:
            yield cast('N', self)


# Empty trees are just None
# Note that mypy doesn't yet support this, but it's in PEP 484
Tree = Optional[Node[N, V]]  # type: ignore
