import math
import operator

from .mc_tree import MCTNode, State


class UCTNode(MCTNode['UCTNode', State]):  # type: ignore
    def ucb1(self, child: 'UCTNode') -> float:
        return child.wins / child.visits + math.sqrt(2 * math.log(self.visits) / child.visits)

    def select_child(self):
        return max(
            ((child, self.ucb1(child)) for child in self.children),
            key=operator.itemgetter(1)
        )[0]
