from typing import Generic, List, Optional, TypeVar

T = TypeVar('T')


class Node(Generic[T]):
    """An abstract multi-child tree"""

    def __init__(self, value: T):
        self.value = value

        self._children = []
        self._parent = None

    @property
    def children(self):
        return self.children

    @children.setter
    def children(self, children: List["Node"[T]]=[]):
        for child in children:
            child._parent = self
        self._children = children

    @property
    def parent(self):
        return self._parent

    def add_children(self, children: List["Node"[T]]=[]):
        self.children = self.children + children
        return self

    def add_child(self, child: "Node"[T]):
        self.add_children([child])
        return self


# Empty trees are just None
Tree = Optional[Node[T]]
