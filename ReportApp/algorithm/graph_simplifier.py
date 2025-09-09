from ReportApp.algorithm.my_graph import _Graph


class _GraphSimplifier:
    
    def simplify_greedy(self, graph: _Graph):
        sub_ids = graph._node_degrees.keys()
        sub_vals = graph._node_degrees.values()
        edges_list = self._build_edges_greedy(sub_ids, sub_vals)
        return edges_list
    
    
    def _build_edges_greedy(self, sub_ids, sub_vals):
        debtors = []
        creditors = []
        for idx, val in zip(sub_ids, sub_vals):
            if val < 0:
                debtors.append([idx, val])
            elif val > 0:
                creditors.append([idx, val])
        d, c = 0, 0
        edges = []
        while d < len(debtors) and c < len(creditors):
            di, dbal = debtors[d]
            ci, cbal = creditors[c]
            amount = min(-dbal, cbal)
            edges.append((di, ci, amount))
            debtors[d][1] += amount
            creditors[c][1] -= amount
            if debtors[d][1] == 0: d += 1
            if creditors[c][1] == 0: c += 1
        return edges
