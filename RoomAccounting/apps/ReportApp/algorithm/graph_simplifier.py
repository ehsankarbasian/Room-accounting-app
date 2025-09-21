from functools import lru_cache

from apps.ReportApp.algorithm.report_graph import _Graph


class _GraphSimplifier:
    
    @staticmethod
    def simplify_greedy(graph: _Graph):
        nodes = graph.nodes
        degrees = graph.degrees
        return _GraphSimplifier._build_edges_greedy(nodes, degrees)
    
    
    @staticmethod
    def simplify_dynamic(graph: _Graph):
        balances = graph.non_zero_node_degrees
        return _GraphSimplifier._build_edges_dynamic(balances)
    
    
    @staticmethod
    def _build_edges_greedy(nodes, degrees):
        
        debtor_nodes = []
        creditor_nodes = []
        for node, degree in zip(nodes, degrees):
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
    
    
    @staticmethod
    def _build_edges_dynamic(balances: dict):
        node_count = len(balances)
        if node_count == 0:
            return []
        
        degrees = list(balances.values())
        nodes = list(balances.keys())

        # PreCalculate subset sums
        subset_count = 1 << node_count # 2**node_count
        subset_sums = [0] * subset_count
        for subset_mask in range(1, subset_count):
            last = (subset_mask & -subset_mask).bit_length() - 1
            prev = subset_mask ^ (1 << last)
            subset_sums[subset_mask] = subset_sums[prev] + degrees[last]
    

        @lru_cache(None)
        def get_best_edges(candid_mask):
            if candid_mask == 0:
                return 0, []
            
            best_match = (-1, [])
            subset_to_analyze = candid_mask
            
            while subset_to_analyze:
                if subset_sums[subset_to_analyze] == 0:
                    rest_mask = candid_mask ^ subset_to_analyze
                    rest_edge_count, rest_edges = get_best_edges(rest_mask)
                    
                    subset_nodes = [nodes[i] for i in range(node_count) if (subset_to_analyze>>i)&1]
                    subset_degrees = [degrees[i] for i in range(node_count) if (subset_to_analyze>>i)&1]
                    subset_edges = _GraphSimplifier._build_edges_greedy(subset_nodes, subset_degrees)
                    total_edge_count = 1 + rest_edge_count
                    if total_edge_count > best_match[0]:
                        best_match = (total_edge_count, rest_edges + subset_edges)
                
                subset_to_analyze = (subset_to_analyze-1) & candid_mask
            
            return best_match

        initial_candid_mask = subset_count - 1
        _, edges = get_best_edges(initial_candid_mask)
        return edges
