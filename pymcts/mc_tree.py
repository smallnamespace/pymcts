import operator
import random

from .tree import Node
from abc import ABCMeta, abstractmethod, abstractproperty
from copy import deepcopy
from typing import cast, Dict, Generic, Iterable, Hashable, List, Optional, TypeVar

PlayerIdx = int
Result = Dict[PlayerIdx, float]


class State(metaclass=ABCMeta):
    @abstractproperty
    def result(self) -> Optional[Result]:
        """
        Payoff for each player, indexed by the player id.

        None for non-terminal nodes.
        """
        pass

    @abstractproperty
    def moves(self) -> Iterable[Hashable]:
        pass

    @abstractproperty
    def previous_player(self) -> PlayerIdx:
        pass

    @abstractmethod
    def do_move(self, move) -> None:
        pass

    def rollout(self) -> Result:
        """Override this for a faster roll-out that doesn't depend on state copying"""
        state = deepcopy(self)
        while state.moves:
            state.do_move(random.choice(tuple(state.moves)))
        return state.result

N = TypeVar('N')


class MCTNode(Node[N, State], Generic[N]):
    def __init__(self, state: State, children: Iterable[N]=None, move: Hashable=None) -> None:
        self.move = move
        self._untried_moves = set(state.moves)  # type: Set[Hashable]
        self._wins = 0.0
        self._visits = 0.0
        super().__init__(state, children)

    @property
    def state(self):
        return self.value

    @property
    def wins(self):
        return self._wins

    @property
    def visits(self):
        return self._visits

    @property
    def terminal(self) -> bool:
        return not (self._untried_moves or self.children)

    def expand(self) -> N:
        move = random.choice(tuple(self._untried_moves))
        self._untried_moves.remove(move)
        new_state = deepcopy(self.state)
        new_state.do_move(move)
        child = self.__class__(state=new_state, move=move)  # type: ignore
        self.children.append(child)

        return cast('N', child)

    def select(self) -> List[N]:
        node = self
        path = [self]
        while not node._untried_moves and node.children:
            node = cast('MCTNode[N]', node.select_child())
            path.append(node)

        return cast(List[N], path)

    def mc_round(self):
        path = self.select()
        leaf = path[-1]
        if leaf._untried_moves:
            leaf = leaf.expand()
            path.append(leaf)
        result = leaf.state.rollout()
        for node in path:
            node.update(result)

    def best_move(self) -> Optional[Hashable]:
        if not self.children:
            return None

        return max(((child.move, child.visits) for child in cast(List['MCTNode'], self.children)),
                   key=operator.itemgetter(1))[0]

    def select_child(self) -> N:
        return random.choice(self._children)

    def update(self, result: Dict[PlayerIdx, float]) -> N:
        self._visits += 1
        self._wins += result[self.state.previous_player]

    def node_repr(self) -> str:
        """String representation of the node's members, not including children."""
        return 'M: {}, P{}, Wins/Visits: {}/{}, # Untried: {}'.format(
            self.move,
            self.state.previous_player,
            self._wins,
            self._visits,
            len(self._untried_moves))


MCTree = Optional[MCTNode[MCTNode, State]]  # type: ignore
