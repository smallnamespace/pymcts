"""
Convert trees to various kinds of graphs for visualization.
"""

import igraph

from ..mc_tree import MCTree, MCTNode
from ..uct import UCTNode
from typing import Any, Dict


def to_igraph(mct: MCTree=None, max_depth: int=2) -> igraph.Graph:
    g = igraph.Graph(directed=True)
    if not mct:
        return g

    g.add_vertex(id(mct),
                 nodeid=id(mct),
                 path_prob = 1.0,
                 node_prob = 1.0,
                 #score = 1.0,
                 **node_attributes(None, mct))
    pyid_to_vid = {id(mct): 0}

    next_vid = 1
    for parent in mct.traverse(max_depth=max_depth - 1):
        child_vs = []
        child_score_sum = 0
        for child in parent.children:
            g.add_vertex(id(child),
                         nodeid=id(child),
                         **node_attributes(parent, child))
            pyid_to_vid[id(child)] = next_vid
            g.add_edge(pyid_to_vid[id(parent)],
                       next_vid,
                       move=child.move)

            v = g.vs[next_vid]
            child_vs.append(v)
            child_score_sum += v['score']
            next_vid += 1

        # Go back and set probs on each child node and each edge
        parent_v = g.vs[pyid_to_vid[id(parent)]]
        for child_v in child_vs:
            # For UCT, 'score' is the instaneous marginal change in the ucb1 score for an
            # additional visit to the child node; here we reweight the score of a child in
            # proportion to its siblings
            prob = child_v['score'] / child_score_sum
            path_prob = prob * parent_v['path_prob']
            child_v['node_prob'] = prob
            child_v['path_prob'] = path_prob
            for eid in g.incident(child_v, mode='in'):
                e = g.es[eid]
                e['node_prob'] = prob
                e['path_prob'] = path_prob
    return g


def node_attributes(parent: MCTNode, child: MCTNode) -> Dict[str, Any]:
    if parent:
        score = (parent.ucb1_grad(child)
                 if isinstance(parent, UCTNode) and isinstance(child, UCTNode)
                 else child.visits)
    else:
        score = 1.0
    return dict(
        state=repr(child.state),
        wins=child.wins,
        visits=child.visits,
        ratio=child.wins / child.visits,
        score=score,
        untried=len(child._untried_moves)
    )
