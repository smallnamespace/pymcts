from enum import Enum
from typing import cast, Any, Generator, Generic, Iterable, List, Optional, TypeVar, Union, Tuple

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

    def traverse_edges(self,
                       order=Traversal.preorder,
                       max_depth=None,
                       parent: 'N'=None) -> Generator[Tuple['N', 'N'], Any, Tuple['N', 'N']]:
        """
        Traverse edges of tree rooted at this node. Results are undefined if the tree is modified
        concurrently.

        Note: Results will include an implicit edge from None to the root.

        :param order: Pre-order results in natural DFS edge ordering; post-order results in child
        edges being yielded first
        :param return_tuples: if True, returns a tuple of (parent, node) rather than just node
        :param max_depth: cut off traversal below this depth; a singleton node has depth of 1
        """
        if (max_depth is not None) and max_depth < 1:
            return  # type: ignore

        if order == Traversal.preorder:
            yield parent, cast('N', self)

        for child in self.children:
            yield from cast('Node', child).traverse_edges(order,
                                                          max_depth - 1 if max_depth else None,
                                                          self)

        if order == Traversal.postorder:
            yield parent, cast('N', self)

    def traverse(self,
                 order=Traversal.preorder,
                 max_depth=None,
                 parent: 'N' = None) -> Generator['N', Any, 'N']:
        """
        Traverse tree rooted at this node. Results are undefined if the tree is modified
        concurrently.

        :param max_depth: cut off traversal below this depth; a singleton node has depth of 1
        """
        for _, child in self.traverse_edges(order, max_depth, parent):
            yield child

# Empty trees are just None
# Note that mypy doesn't yet support this, but it's in PEP 484
Tree = Optional[Node[N, V]]  # type: ignore
