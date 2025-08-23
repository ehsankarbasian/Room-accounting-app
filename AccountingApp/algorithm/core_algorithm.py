from AccountingApp.algorithm.graph import ReportGraph


def calculate_room_result(room):##
    return ReportGraph(room)


def is_room_cleared(graph):
    return len(graph.edges()) == 0


def cleared_person(person):##
    graph = calculate_room_result(person.room)
    for k, j in graph.edges():
        v = graph.get_edge_data(k, j)['weight']
        if v != 0 and person.id in [k, j]:
            return True
    return False
