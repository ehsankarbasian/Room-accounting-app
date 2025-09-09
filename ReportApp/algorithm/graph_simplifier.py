from ReportApp.algorithm.report_graph import _ReportGraph


def _adapt_graph(graph):
    in_degree = graph.in_degree(weight='weight')
    out_degree = graph.out_degree(weight='weight')
    result = {}
    for in_, out in zip(in_degree, out_degree):
        node_id = in_[0]
        in_degree = in_[1]
        out_degree = out[1]
        result[node_id] = in_degree - out_degree
    
    return result


def _reverse_adapt_graph(edges_list):
    adapted_dict = {}
    for edge in edges_list:
        before = adapted_dict.get(edge[0], None)
        if before is None:
            adapted_dict[edge[0]] = {edge[1]: {'weight': edge[2]}}
        else:
            before[edge[1]] = {'weight': edge[2]}
            adapted_dict[edge[0]] = before
    
    graph = _ReportGraph(room=None, incoming_graph_data=adapted_dict)
    return graph


class _GraphSimplifier:
    
    def simplify_greedy(self, graph):
        graph_dict = _adapt_graph(graph)
        graph_dict = {k: v for k, v in sorted(graph_dict.items(), key=lambda item: item[1])}
        sub_ids = graph_dict.keys()
        sub_vals = graph_dict.values()
        edges_list = self._build_edges_greedy(sub_ids, sub_vals)
        return _reverse_adapt_graph(edges_list)
    
    
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
