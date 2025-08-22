import networkx
import matplotlib.pyplot as plt


from networkx import DiGraph as DirectedGraph


class AggregateDirectedGraph(DirectedGraph):
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
        
        return super().add_edge(u_of_edge, v_of_edge, **kwargs)


def display_graph(grapg):
    pos = networkx.spring_layout(grapg)  
    weight_labels = networkx.get_edge_attributes(grapg, 'weight')  
    networkx.draw(grapg, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=700)
    networkx.draw_networkx_edge_labels(grapg, pos, edge_labels=weight_labels)  
    plt.show()
    print('end')


graph = AggregateDirectedGraph()
# graph.add_nodes_from()

graph.add_edge(4, 2, weight=-5)
graph.add_edge(0, 4, weight=2)
graph.add_edge(1, 3, weight=1)
graph.add_edge(5, 3, weight=1)
graph.add_edge(5, 3, weight=2)
graph.add_edge(5, 3, weight=-1)
graph.add_edge(3, 5, weight=7)
graph.add_edge(5, 0, weight=-4)

display_graph(graph)
