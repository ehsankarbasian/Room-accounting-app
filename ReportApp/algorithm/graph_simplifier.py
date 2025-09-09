from functools import lru_cache

from ReportApp.algorithm.report_graph import _Graph


class _MockGraph:
    
    def __init__(self, nodes, degrees):
        self.node_degrees = dict(zip(nodes, degrees))


class _GraphSimplifier:
    
    def simplify_greedy(self, graph: _Graph):
        return self._build_edges_greedy(graph)
    
    
    def simplify_dynamic(self, graph: _Graph):
        balances = graph.node_degrees
        
        # مرتب کنیم طبق اندیس
        n = max(balances.keys())+1
        arr = [balances.get(i,0) for i in range(n)]
        
        min_e, edges = self._min_transactions_with_edges(arr)
        return edges
    
    
    def _build_edges_greedy(self, graph: _Graph):
        
        debtor_nodes = []
        creditor_nodes = []
        for node, degree in graph.node_degrees.items():
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
    
    
    def _build_edges_greedy_in_dp(self, sub_ids, sub_vals):
        graph = _MockGraph(sub_ids, sub_vals)
        return self._build_edges_greedy(graph)
        
    
    
    def _min_transactions_with_edges(self, balances):
        nums = [b for b in balances if b != 0]
        ids  = [i for i,b in enumerate(balances) if b != 0]
        n = len(nums)
        if n == 0:
            return 0, []

        # پیش‌محاسبه مجموع هر subset
        subset_sum = [0] * (1 << n)
        for mask in range(1, 1 << n):
            last = (mask & -mask).bit_length() - 1
            prev = mask ^ (1 << last)
            subset_sum[mask] = subset_sum[prev] + nums[last]
    

        @lru_cache(None)
        def dp(mask):
            if mask == 0:
                return (0, [])
            best = (-1, [])
            sub = mask
            while sub:
                if subset_sum[sub] == 0:
                    rest_mask = mask ^ sub
                    val_rest, edges_rest = dp(rest_mask)
                    # این subset رو با |S|-1 یال حل می‌کنیم
                    sub_ids = [ids[i] for i in range(n) if (sub>>i)&1]
                    sub_vals = [nums[i] for i in range(n) if (sub>>i)&1]
                    edges_sub = self._build_edges_greedy_in_dp(sub_ids, sub_vals)
                    val_total = 1 + val_rest  # یه گروه صفر بیشتر
                    if val_total > best[0]:
                        best = (val_total, edges_rest + edges_sub)
                sub = (sub-1) & mask
            return best

        max_groups, edges = dp((1<<n)-1)
        min_edges = n - max_groups
        return min_edges, edges
