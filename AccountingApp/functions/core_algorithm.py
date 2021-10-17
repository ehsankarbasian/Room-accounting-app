from AccountingApp.models import *


def calculate_result(room):
    persons = list(room.person_set.all())
    result_dict = initial_result_dict(persons)

    result_dict = calculate_room_result(room, result_dict)
    result_dict = impact_transactions(room, result_dict)

    result_dict = reverse_negatives(result_dict)
    result_dict = replace_person_id_with_name(result_dict)

    return result_dict


def initial_result_dict(persons):
    result_dict = dict({})
    max_index = len(persons) - 1
    for p1 in persons:
        p1_index = persons.index(p1)
        if p1_index < max_index:
            remaining_persons = persons[p1_index + 1:]
            for p2 in remaining_persons:
                result_dict[str(p1.id) + '  ---->  ' + str(p2.id)] = 0

    return result_dict


def calculate_room_result(room, result_dict):
    spend_list = spend_list_generator(room)

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

        for k, v in result_dict.items():
            spender_to_partner = spender_dict[int(k.split()[0])] and partner_dict[int(k.split()[2])]
            partner_to_spender = partner_dict[int(k.split()[0])] and spender_dict[int(k.split()[2])]

            if spender_to_partner:
                partnership_ratio = partner_dict[int(k.split()[2])] / partners_sum_of_weight
                spendership_ratio = spender_dict[int(k.split()[0])] / spenders_sum_of_weight

                result_dict[k] -= amount * partnership_ratio * spendership_ratio

            if partner_to_spender:
                partnership_ratio = (partner_dict[int(k.split()[0])] / partners_sum_of_weight)
                spendership_ratio = (spender_dict[int(k.split()[2])] / spenders_sum_of_weight)

                result_dict[k] += amount * partnership_ratio * spendership_ratio

    return result_dict


def spend_list_generator(room):
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


def impact_transactions(room, result_dict):
    transactions = room.transaction_set
    for transaction in transactions:
        payer_id = transaction.payer.id
        receiver_id = transaction.receiver.id
        amount = transaction.amount
        for k, v in result_dict.items():
            if payer_id == int(k.split()[0]) and receiver_id == int(k.split()[2]):
                result_dict[k] -= amount
            elif payer_id == int(k.split()[2]) and receiver_id == int(k.split()[0]):
                result_dict[k] += amount

    return result_dict


def reverse_negatives(result_dict):
    final_dict = {}
    for k, v in result_dict.items():
        key_lst = k.split()
        if v < 0:
            key_lst = key_lst[::-1]
        key = key_lst[0] + ' ' + key_lst[1] + ' ' + key_lst[2]
        final_dict[key] = int(abs(v))

    return final_dict


def replace_person_id_with_name(result_dict):
    result = dict({})
    for k, v in result_dict.items():
        person_1 = Person.objects.get(id=int(k.split()[0]))
        person_2 = Person.objects.get(id=int(k.split()[2]))
        key = person_1.name + " --> " + person_2.name
        value = [v, person_1, person_2]
        result[key] = value

    return result


def simple_result(final_dict):
    result = dict({})
    for k, v in final_dict.items():
        result[k] = v[0]

    return result


def is_room_cleared(final_dict):
    cleared = 1
    for k, v in final_dict.items():
        if v[0]:
            cleared = 0
    return cleared
