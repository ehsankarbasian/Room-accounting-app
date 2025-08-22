import networkx
import matplotlib.pyplot as plt


from networkx import DiGraph as _DirectedGraph


class AggregateDirectedGraph(_DirectedGraph):
    # TODO: test and refactor
    
    def add_edge(self, u_of_edge, v_of_edge, **kwargs):
        if kwargs.get('weight', None) is not None:
            if self.has_edge(u_of_edge, v_of_edge):
                previous_weight = self.get_edge_data(u_of_edge, v_of_edge)['weight']
                kwargs['weight'] += previous_weight
            elif self.has_edge(v_of_edge, u_of_edge):
                previous_weight = self.get_edge_data(v_of_edge, u_of_edge)['weight']
                kwargs['weight'] -= previous_weight
                if self.has_edge(v_of_edge, u_of_edge):
                    self.remove_edge(v_of_edge, u_of_edge)
        
        if kwargs.get('weight') < 0:
            if self.has_edge(u_of_edge, v_of_edge):
                self.remove_edge(u_of_edge, v_of_edge)
            u_of_edge, v_of_edge = v_of_edge, u_of_edge
            kwargs['weight'] = -kwargs['weight']
        if kwargs.get('weight') == 0:
            self.remove_edge(u_of_edge, v_of_edge)
            return
            # self.remove_edge(v_of_edge, u_of_edge)
        
        return super().add_edge(u_of_edge, v_of_edge, **kwargs)
    
    
    def simplifiy_graph_cycle(self):
        cycles = list(networkx.simple_cycles(self))
        for cycle in cycles:
            cycle_weights = [self.get_edge_data(cycle[i], cycle[i+1])['weight'] for i in range(len(cycle) - 1)]
            cycle_weights += [self.get_edge_data(cycle[-1], cycle[0])['weight']]
            
            min_weight = min(cycle_weights)
            for i in range(len(cycle) - 1):
                self.add_edge(cycle[i], cycle[i+1], weight=-min_weight)
            self.add_edge(cycle[-1], cycle[0], weight=-min_weight)
    
    
    def simplify_graph_path(self):
        pass
    
    
    @property
    def sorted_graph_by_weight(self):
        weight_labels = networkx.get_edge_attributes(self, 'weight')
        return {k: v for k, v in sorted(weight_labels.items(), key=lambda item: item[1], reverse=True)}


def display_graph(graph):
    pos = networkx.spring_layout(graph)
    sorted_graph = graph.sorted_graph_by_weight
    networkx.draw(graph, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=700)
    networkx.draw_networkx_edge_labels(graph, pos, edge_labels=sorted_graph)
    plt.show()
    print('End')


graph = AggregateDirectedGraph()
# graph.add_nodes_from()

graph.add_edge(4, 2, weight=-5)
graph.add_edge(0, 4, weight=2)
graph.add_edge(1, 3, weight=1)
graph.add_edge(5, 3, weight=1)
graph.add_edge(5, 1, weight=4)
graph.add_edge(5, 3, weight=2)
graph.add_edge(5, 3, weight=-1)
graph.add_edge(3, 5, weight=7)
graph.add_edge(5, 0, weight=-4)

graph.simplifiy_graph_cycle()

display_graph(graph)
