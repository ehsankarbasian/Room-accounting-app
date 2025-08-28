from django.test import TestCase, Client

from ReportApp.models import Transaction
from ReportApp.apps import ReportAppConfig


def _client_post(url, json):
    response = Client().post("/" + ReportAppConfig.name + "/" + url, json, format='json')
    return response.data


def create_transactions():
    Transaction.objects.create(amount=3500, payer_id=1, receiver_id=2)
    Transaction.objects.create(amount=625, payer_id=5, receiver_id=7)
    Transaction.objects.create(amount=2375, payer_id=4, receiver_id=6)
    Transaction.objects.create(amount=1500, payer_id=2, receiver_id=3)
    Transaction.objects.create(amount=2625, payer_id=6, receiver_id=7)
    Transaction.objects.create(amount=700, payer_id=1, receiver_id=2)
    Transaction.objects.create(amount=6250, payer_id=5, receiver_id=6)


class CoreAlgorithmTestCase(TestCase):

    fixtures = ['user.json', 'room.json', 'person.json', 'spend.json', 'spender_partner.json']

    def test_result(self):
        response_1 = _client_post('reportForClearingAPI', {"room_id": 1})
        response_2 = _client_post('reportForClearingAPI', {"room_id": 2})


        print()
        print()
        print(response_1)
        print(type(response_1))
        print()
        print()

        response_1_result = {'1 --> 2': 6000, '1 --> 3': 11500,
                             '2 --> 3': 1500}
        response_2_result = {'5 --> 4': 7500, '4 --> 6': 22375,
                             '7 --> 4': 5250, '5 --> 6': 26250,
                             '7 --> 5': 2375, '7 --> 6': 12375}

        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)

    def test_result_with_transactions(self):
        create_transactions()

        response_1 = _client_post('reportForClearingAPI', {"room_id": 1})
        response_2 = _client_post('reportForClearingAPI', {"room_id": 2})

        response_1_result = {'1 --> 2': 1800, '1 --> 3': 11500}
        response_2_result = {'5 --> 4': 7500, '4 --> 6': 20000,
                             '7 --> 4': 5250, '5 --> 6': 20000,
                             '7 --> 5': 3000, '7 --> 6': 15000}

        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)
