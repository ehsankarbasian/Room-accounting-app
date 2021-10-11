from django.test import TestCase

from AccountingApp.models import *
from .functions.helper_functions import client_post


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
        response_1 = client_post('reportForClearingAPI', {"room_id": 1})
        response_2 = client_post('reportForClearingAPI', {"room_id": 2})

        response_1_result = {'person_1 --> person_2': 6000, 'person_1 --> person_3': 11500,
                             'person_2 --> person_3': 1500}
        response_2_result = {'person_5 --> person_4': 7500, 'person_4 --> person_6': 22375,
                             'person_7 --> person_4': 5250, 'person_5 --> person_6': 26250,
                             'person_7 --> person_5': 2375, 'person_7 --> person_6': 12375}

        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)

    def test_result_with_transactions(self):
        create_transactions()

        response_1 = client_post('reportForClearingAPI', {"room_id": 1})
        response_2 = client_post('reportForClearingAPI', {"room_id": 2})

        response_1_result = {'person_1 --> person_2': 1800, 'person_1 --> person_3': 11500,
                             'person_2 --> person_3': 0}
        response_2_result = {'person_5 --> person_4': 7500, 'person_4 --> person_6': 20000,
                             'person_7 --> person_4': 5250, 'person_5 --> person_6': 20000,
                             'person_7 --> person_5': 3000, 'person_7 --> person_6': 15000}

        self.assertEqual(response_1, response_1_result)
        self.assertEqual(response_2, response_2_result)
