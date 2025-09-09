from itertools import combinations as get_subsets

from ReportApp.models import Room
from ReportApp.algorithm.room_analyzer import _RoomAnalyzer


class _Graph:
    """
    Not really a graph
    Acts like a graph but it is more simple than a graph
    
    differences:
        Only saves degree of each node (weighted degree)
        It's the only thing that the algorithm cares about
        So not to save additional info like directed edges
    """
    
    def __init__(self, room: Room):
        person_id_list = room.person_set.values_list('id', flat=True)
        self._node_degrees = {person_id: 0 for person_id in person_id_list}
        
        self.potential_edges = list(get_subsets(person_id_list, 2))
        
        _RoomAnalyzer.calculate_room_spend_result(room, self)
        _RoomAnalyzer.calculate_room_transaction_result(room, self)
    
    @property
    def node_degrees(self):
        return self._node_degrees
    
    def add_edge(self, k, v, weight=1):
        self._node_degrees[k] -= weight
        self._node_degrees[v] += weight
    
    
    @property
    def _graph_schema(self):
        # TEMP: just to pass algorithm functionality test
        result = {}
        for u, v in self.edges_sorted:
            w = int(self.get_edge_weight(u, v))
            result[f'{u} --> {v}'] = w
        
        return result
