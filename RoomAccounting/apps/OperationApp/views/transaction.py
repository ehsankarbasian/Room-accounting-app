from django.views.generic.base import View
from django.shortcuts import redirect

from apps.ReportApp.models import Person, Transaction

from apps.AuthApp.persmissions.mixins import PermissionMixin
from apps.AuthApp.persmissions.permissions import IsAuthenticated

from .utils import result_page


class AddTransactionView(PermissionMixin, View):
    
    permission_classes = (IsAuthenticated, )
    
    
    def post(self, request, room_id):
        amount = request.POST['amount']
        payer_id = request.POST['Payer']
        receiver_id = request.POST['Receiver']

        if payer_id == receiver_id:
            return result_page(request, "ERROR: The payer and the receiver are the same")

        payer = Person.objects.get(id=payer_id)
        receiver = Person.objects.get(id=receiver_id)
        transaction = Transaction.objects.create(amount=amount, payer=payer, receiver=receiver)

        # TODO:
        # EmailGenerator.send_new_transaction_to_person(transaction)
        
        return redirect('ReportApp:home')
