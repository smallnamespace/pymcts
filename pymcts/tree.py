from typing import Generic, List, Optional, TypeVar

T = TypeVar('T')


class Node(Generic[T]):
    """An abstract multi-child tree"""

    def __init__(self, value: T) -> None:
        self.value = value

        self._children = [] # type: List[Node[T]]
        self._parent = None # type: Node[T]

    @property
    def children(self) -> List["Node[T]"]:
        return self._children

    @children.setter
    def children(self, children: List["Node[T]"]=[]) -> None:
        for child in children:
            child._parent = self
        self._children = children

    @property
    def parent(self) -> "Node[T]":
        return self._parent

    def add_children(self, children: List["Node[T]"]=[]):
        self.children = self.children + children
        return self

    def add_child(self, child: "Node[T]"):
        self.add_children([child])
        return self


# Empty trees are just None
# Note that mypy doesn't yet support this, but it's in PEP 484
Tree = Optional[Node[T]]
