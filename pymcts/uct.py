import operator

from .mc_tree import MCTNode, State
from math import log, sqrt


class UCTNode(MCTNode['UCTNode', State]):  # type: ignore
    def ucb1(self, child: 'UCTNode') -> float:
        return child.wins / child.visits + sqrt(2 * log(self.visits) / child.visits)

    def ucb1_grad(self, child: 'UCTNode') -> float:
        """
        Even though UCT is a deterministic algorithm (up to tie breaks when nodes are equal),
        we can determine the marginal sampling rate of each node in the immediate future by
        calculating how its ucb1 score changes over the next iteration.

        See http://sagecell.sagemath.org/?z=eJydkdFKwzAUhu8He4cDu9iJxjWJ7MILn2SMMtdOCjGdTZPMt_ePmSJb3YVQOPTLn4__kCQp4jtKSgbT0DPF3cDLRBEUEGwp5rPA6ZwUiKQq0j3592FkQ3dkHWdeUURyPjvlhKkgm8wYQQ_EfyvgSLXvrYMGI7Z8QjuxUdssX5Sz1SFYW_vu7Wi7wwcLSaH24eUS49_tx66H3XyvmbOXOXgXyRSzYy2NfJTrr2UatAir12HXdK0bc5JTronODSphh2ajyzBbqG-dXpdmjfStK1d3cie_74eWf17jP5Ki0JK0UkpgZ5QpbK3UBH2apBn8wmftJ8wPoug=&lang=sage
        for derivation.

        :return: Let grad(u) be the gradient of ucb1. Then this calculates -1 / grad(u) * <1, 1>;
        i.e. the  negative inverse change in ucb1 score given a unit increase in parent and
        child visits.
        """
        v = child.visits
        vp = self.visits
        return (sqrt(2)*v*v*vp*sqrt(log(vp)/v) /
                (vp*log(vp) - v))

    def select_child(self):
        return max(
            ((child, self.ucb1(child)) for child in self.children),
            key=operator.itemgetter(1)
        )[0]
