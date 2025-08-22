from AccountingApp.models import Person
from AccountingApp.algorithm.graph import AggregateDirectedGraph


def __calculate_result_of_room(room):
    graph = AggregateDirectedGraph(potential_edges=__get_room_potential_edges(room))
    
    graph = __calculate_room_result(room, graph)
    graph = __impact_transactions(room, graph)

    return graph


def calculate_result(room):##
    graph = __calculate_result_of_room(room)
    return graph


def __get_room_potential_edges(room):
    persons = list(room.person_set.all())
    
    potential_edges = []
    max_index = len(persons) - 1
    for p1 in persons:
        p1_index = persons.index(p1)
        if p1_index < max_index:
            remaining_persons = persons[p1_index + 1:]
            for p2 in remaining_persons:
                potential_edges.append((p1.id, p2.id))

    return potential_edges


def __calculate_room_result(room, graph):
    spend_list = __spend_list_generator(room)

    for spend in spend_list:
        amount = spend['amount']
        spender_dict = spend['spender_dict']
        partner_dict = spend['partner_dict']

        partners_sum_of_weight = 0
        spenders_sum_of_weight = 0
        for k, v in partner_dict.items():
            partners_sum_of_weight += partner_dict[k]
        for k, v in spender_dict.items():
            spenders_sum_of_weight += spender_dict[k]
        for k, v in graph.potential_edges:
            spender_to_partner = spender_dict[k] and partner_dict[v]
            partner_to_spender = partner_dict[k] and spender_dict[v]

            if spender_to_partner:
                partnership_ratio = partner_dict[v] / partners_sum_of_weight
                spendership_ratio = spender_dict[k] / spenders_sum_of_weight

                weight = -amount * partnership_ratio * spendership_ratio
                graph.add_edge(k, v, weight=weight)

            if partner_to_spender:
                partnership_ratio = (partner_dict[k] / partners_sum_of_weight)
                spendership_ratio = (spender_dict[v] / spenders_sum_of_weight)

                weight = amount * partnership_ratio * spendership_ratio
                graph.add_edge(k, v, weight=weight)

    return graph


def __spend_list_generator(room):
    spend_list = []
    for spend in room.spend_set.all():
        amount = spend.amount

        partner_dict = spend.partner_dict()
        partners_sum_of_weight = 0
        for k, v in partner_dict.items():
            partners_sum_of_weight += partner_dict[k]

        spender_dict = spend.spender_dict()
        spenders_sum_of_weight = 0
        for k in spender_dict:
            spenders_sum_of_weight += spender_dict[k]

        the_spent = {'amount': amount,
                     'partner_dict': partner_dict,
                     'spender_dict': spender_dict}

        spend_list.append(the_spent)

    return spend_list


def __impact_transactions(room, graph):
    transactions = room.transaction_set
    for transaction in transactions:
        payer_id = transaction.payer.id
        receiver_id = transaction.receiver.id
        amount = transaction.amount
        for k, v in graph.potential_edges:
            if payer_id == k and receiver_id == v:
                graph.add_edge(k, v, weight=-amount)
            elif payer_id == v and receiver_id == k:
                graph.add_edge(k, v, weight=amount)

    return graph


def is_room_cleared(graph):
    return len(graph.edges()) == 0


def cleared_person(person):##
    graph = __calculate_result_of_room(person.room)
    for k, j in graph.edges():
        v = graph.get_edge_data(k, j)['weight']
        if v != 0 and person.id in [k, j]:
            return True
    return False
