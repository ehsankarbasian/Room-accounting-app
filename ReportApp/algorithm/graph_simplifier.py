from ReportApp.algorithm.report_graph import _Graph


class _GraphSimplifier:
    
    def simplify_greedy(self, graph: _Graph):
        return self._build_edges_greedy(graph)
    
    
    def _build_edges_greedy(self, graph: _Graph):
        
        debtor_nodes = []
        creditor_nodes = []
        for node, degree in graph.node_degrees:
            if degree < 0:
                debtor_nodes.append([node, degree])
            elif degree > 0:
                creditor_nodes.append([node, degree])
        
        edges = []
        debtor_index = 0
        creditor_index = 0
        while debtor_index < len(debtor_nodes) and creditor_index < len(creditor_nodes):
            debtor_node, debtor_degree = debtor_nodes[debtor_index]
            creditor_node, creditor_degree = creditor_nodes[creditor_index]
            amount_to_match = min(-debtor_degree, creditor_degree)
            
            new_edge = (debtor_node, creditor_node, amount_to_match)
            edges.append(new_edge)
            
            debtor_nodes[debtor_index][1] += amount_to_match
            creditor_nodes[creditor_index][1] -= amount_to_match
            
            if debtor_nodes[debtor_index][1] == 0:
                debtor_index += 1
            if creditor_nodes[creditor_index][1] == 0:
                creditor_index += 1
        
        return edges
