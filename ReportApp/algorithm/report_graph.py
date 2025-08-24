from networkx import DiGraph as _DirectedGraph

from ReportApp.algorithm.room_analyzer import RoomAnalyzer


class ReportGraph(_DirectedGraph):
    
    def __init__(self, room, incoming_graph_data=None, **attr):
        super().__init__(incoming_graph_data, **attr)
        # If delete the line above, Error will happen:
        # '_CachedPropertyResetterAdjAndSucc' object is not subscriptable
        
        self._room = room
        self.potential_edges = RoomAnalyzer.get_room_potential_edges(room)
        RoomAnalyzer.calculate_room_spend_result(room, self)
        RoomAnalyzer.calculate_room_transaction_result(room, self)
    
    def get_edge_weight(self, v, u):
        # if not self.has_edge(v, u):
            # return 0
        return self.get_edge_data(v, u)['weight']
    
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
            try:
                self.remove_edge(u_of_edge, v_of_edge)
                return
            except:
                return
            # self.remove_edge(v_of_edge, u_of_edge)
        
        super().add_edge(u_of_edge, v_of_edge, **kwargs)
    
    
    @property
    def edges_sorted(self):
        return sorted(self.edges(), key=lambda edge: self.get_edge_weight(*edge), reverse=True)
