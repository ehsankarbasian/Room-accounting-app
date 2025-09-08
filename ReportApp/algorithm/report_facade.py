from .report_graph import _ReportGraph
from .room_analyzer import _RoomAnalyzer
from .graph_simplifier import _GraphSimplifier


class ReportFacade:
    
    @staticmethod
    def is_room_cleared(room):
        return _RoomAnalyzer.is_room_cleared(room)
    
    @staticmethod
    def get_graph(room):
        graph = _ReportGraph(room)
        simple_graph = _GraphSimplifier.simplifiy_graph_cycle(graph)
        return simple_graph
