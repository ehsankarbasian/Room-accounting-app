from ReportApp.models import Room


class _RoomAnalyzer:
    
    @staticmethod
    def is_room_cleared(graph):
        return len(graph) == 0
    
    
    @staticmethod
    def calculate_room_spend_result(room: Room, graph):
        spend_list = _RoomAnalyzer._spend_list_generator(room)

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
    
    
    @staticmethod
    def _spend_list_generator(room: Room):
        # PERFORMANCE: Use prefetch data to avoid N+1 problem
        spend_list = []
        for spend in room.spend_set.all():
            partner_dict = spend.partner_dict
            partners_sum_of_weight = 0
            for k, v in partner_dict.items():
                partners_sum_of_weight += partner_dict[k]

            spender_dict = spend.spender_dict
            spenders_sum_of_weight = 0
            for k in spender_dict:
                spenders_sum_of_weight += spender_dict[k]

            the_spent = {'amount': spend.amount,
                        'partner_dict': partner_dict,
                        'spender_dict': spender_dict}

            spend_list.append(the_spent)

        return spend_list
    
    
    @staticmethod
    def calculate_room_transaction_result(room: Room, graph):
        # PERFORMANCE: Use prefetch data to avoid N+1 problem
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
