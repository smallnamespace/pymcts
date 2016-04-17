from typing import Any, Generator, Generic, Iterable, List, Optional, TypeVar

T = TypeVar('T')


class Node(Generic[T]):
    """
    A generic tree node. Nodes point to their parents, and nodes may have multiple children.

    TODO: constrain child types to be polymorphic; e.g. NodeSubclass only takes NodeSubclass as
    children, rather than any instance of Node. This awaits support at
    https://github.com/python/mypy/issues/689.
    """

    def __init__(self, value: T, children: Iterable['Node[T]']=None) -> None:
        self._children = []  # type: List[Node[T]]
        self.value = value
        if children:
            self.children = children

    @property
    def children(self) -> List['Node[T]']:
        return self._children

    @children.setter
    def children(self, children: Iterable['Node[T]']=None) -> None:
        if children:
            self._children = list(children)

    def __repr__(self, level=0):
        indent = ' ' * 4 * level
        return '{indent}{clz}({value!r}{children})'.format(
            indent=indent,
            clz=self.__class__.__name__,
            value=self.value,
            children=(', [\n' +
                      ',\n'.join(c.__repr__(level+1) for c in self._children) + '\n' +
                      indent + ']') if self._children else '')

    def __eq__(self, other):
        """
        TODO: Is it reasonable to ignore the generic type variable?
        E.g. should Node(2.0) == Node(2) ? Currently this is True
        """
        return (isinstance(other, type(self))
                and self.value == other.value
                and self.children == other.children)

    def traverse_postorder(self) -> Generator['Node[T]', Any, 'Node[T]']:
        """
        Traverse tree rooted at this node via post-order DFS. Results are undefined if
        the tree is modified concurrently.
        """
        for child in self.children:
            yield from child.traverse_postorder()
        yield self


# Empty trees are just None
# Note that mypy doesn't yet support this, but it's in PEP 484
Tree = Optional[Node[T]]
