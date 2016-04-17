import operator
import random

from .tree import Node
from abc import ABCMeta, abstractmethod, abstractproperty
from copy import copy
from typing import Dict, Iterable, Hashable, List, Optional

PlayerIdx = int


class State(metaclass=ABCMeta):
    @abstractproperty
    def result(self) -> Optional[Dict[PlayerIdx, float]]:
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
    def do_move(self, move) -> 'State':
        pass


class MCTNode(Node[State]):
    def __init__(self, state: State, children: List['MCTNode']=None, move: Hashable=None):
        self.move = move
        self._untried_moves = set(state.moves)
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

    def expand(self) -> 'MCTNode':
        move = random.choice(tuple(self._untried_moves))
        self._untried_moves.remove(move)
        child = self.__class__(state=self.state.do_move(move), move=move)
        self.children.append(child)

        return child

    def select(self) -> List['MCTNode']:
        node = self
        path = [self]
        while not node._untried_moves and node.children:
            node = node.select_child()
            path.append(node)

        return path

    def mc_round(self):
        path = self.select()
        leaf = path[-1]
        if leaf._untried_moves:
            leaf = leaf.expand()
            path.append(leaf)
        result = leaf.rollout()
        for node in path:
            node.update(result)

    def best_move(self) -> Optional[Hashable]:
        if not self.children:
            return None

        return max(((child.move, child.visits) for child in self.children),
                   key=operator.itemgetter(1))[0]

    def rollout(self) -> Optional[Dict[PlayerIdx, float]]:
        # TODO: Use optional rollout implementation on the state
        state = copy(self.state)
        while state.moves:
            state.do_move(random.choice(tuple(state.moves)))
        return state.result

    def select_child(self) -> 'MCTNode':
        return random.choice(self._children)

    def update(self, result: Dict[PlayerIdx, float]) -> 'MCTNode':
        self._visits += 1
        self._wins += result[self.state.previous_player]


MCTree = Optional[MCTNode]
