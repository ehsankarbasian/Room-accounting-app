import networkx
import matplotlib.pyplot as plt


from networkx import DiGraph as DirectedGraph


def display_graph(grapg):
    pos = networkx.spring_layout(grapg)  
    weight_labels = networkx.get_edge_attributes(grapg, 'weight')  
    networkx.draw(grapg, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=700)
    networkx.draw_networkx_edge_labels(grapg, pos, edge_labels=weight_labels)  
    plt.show()


graph = DirectedGraph()
graph.add_nodes_from(range(5))

graph.add_edge(4, 2, weight=-5)
graph.add_edge(0, 4, weight=2)
graph.add_edge(1, 3, weight=1)
graph.add_edge(5, 3, weight=1)
graph.add_edge(5, 3, weight=2)
graph.add_edge(5, 3, weight=1)
graph.add_edge(3, 5, weight=3)
graph.add_edge(5, 0, weight=4)

display_graph(graph)
