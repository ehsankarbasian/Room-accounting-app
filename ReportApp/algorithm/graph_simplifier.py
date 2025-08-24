import networkx


class GraphSimplifier:
    
    def simplifiy_graph_cycle(graph):
        cycles = list(networkx.simple_cycles(graph))
        for cycle in cycles:
            cycle_weights = [graph.get_edge_data(cycle[i], cycle[i+1])['weight'] for i in range(len(cycle) - 1)]
            cycle_weights += [graph.get_edge_data(cycle[-1], cycle[0])['weight']]
            
            min_weight = min(cycle_weights)
            for i in range(len(cycle) - 1):
                graph.add_edge(cycle[i], cycle[i+1], weight=-min_weight)
            graph.add_edge(cycle[-1], cycle[0], weight=-min_weight)
    
    
    def simplify_graph_donkey_path(graph):
        pass
