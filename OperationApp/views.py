from secrets import token_hex
from itertools import chain
from random import randint

from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.views.generic.base import View

from ReportApp.models import Room, Person, Spend, Spenders, Partners, Transaction
from django.db.models import Q
from RoomAccounting.email_client import send_html_email
from utils.custom_views.views import RawTemplateView
from OperationApp.email_generator import EmailGenerator

from AuthApp.persmissions.mixins import PermissionMixin
from AuthApp.persmissions.permissions import IsAuthenticated


# TODO: Use ModelViews to CRUD


class AddRoomView(PermissionMixin, View):
    permission_classes = (IsAuthenticated, )
    
    def post(self, request):
        room_name = request.POST['room_name']
        Room.objects.create(name=room_name, creator=request.user)
        return redirect('ReportApp:home')


class DeleteRoomView(PermissionMixin, View):
    permission_classes = (IsAuthenticated, )
    
    def post(self, request, room_id):
        room = Room.objects.get(id=room_id)

        if not room.is_owner(request.user):
            return _result_page(request, "You're not the owner of the room")
        
        # TODO: 2 factor auth to delete the room
        room.delete()
        return redirect('ReportApp:home')


class EditRoomView(PermissionMixin, View):
    permission_classes = (IsAuthenticated, )
    
    def post(self, request, room_id):
        room = Room.objects.get(id=room_id)

        if not room.is_owner(request.user):
            return _result_page(request, "You're not the owner of the room")
        
        room.name = request.POST['room_name']
        room.save()
        return redirect('ReportApp:home')


class AddPersonView(PermissionMixin, View):
    permission_classes = (IsAuthenticated, )
    
    def post(self, request, room_id):
        room = Room.objects.get(id=room_id)

        if not room.is_owner(request.user):
            return _result_page(request, "You're not the owner of the room")
        
        name = request.POST['person_name']
        email = request.POST['email']
        phone = request.POST['phone']
        person = Person.objects.create(name=name, email=email, phone=phone, room=room,
                                    verify_email_token=token_hex(64), verify_phone_code=randint(100000, 999999))

        context = {'person_id': person.id,
                    'name': name,
                    'mode': 'verifyPersonEmail',
                    'verify_email_token': person.verify_email_token}
        html_content = get_template('AuthApp/email_verification.html').render(context=context)

        message = "Hello " + name + ". please click on the button below to verify your email"
        send_html_email("Verify email", message, [email], html_content)

        return redirect('ReportApp:home')


class AddSpendView(PermissionMixin, View):
    permission_classes = (IsAuthenticated, )
    
    def post(self, request, room_id):
        room = Room.objects.get(id=room_id)

        if not room.is_owner(request.user):
            return _result_page(request, "You're not the owner of the room")
        
        amount = request.POST['amount']
        description = request.POST['description']
        spend = Spend.objects.create(amount=amount, description=description, room=room)

        # m2m relationships:
        for person in room.person_set.all():
            # Create Spenders
            ID = str(person.id)
            if "spender" + ID in request.POST:
                weight = request.POST['spender_weight' + ID]
                weight = [int(weight) if weight else 1][0]
                Spenders.objects.create(spender_person=person, spender_spend=spend, weight=weight)

            # Create Partners
            if "partner" + ID in request.POST:
                weight = request.POST['person_weight' + ID]
                weight = [int(weight) if weight else 1][0]
                Partners.objects.create(partner_person=person, partner_spend=spend, weight=weight)

        spend = Spend.objects.get(id=spend.id)
        EmailGenerator.send_new_spend_to_person(spend)
        return redirect('ReportApp:home')


# TODO: use ListView
class SpendListView(PermissionMixin, RawTemplateView):
    permission_classes = (IsAuthenticated, )
    template_name = 'ReportApp/list_items/spend.html'
    
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        if not room.is_owner(request.user):
            return _result_page(request, "You're not the owner of the room")
        
        spends = room.spend_set.all().order_by('-date')
        context = {'spends': spends, 'mode': 'spend_log', 'room_name': room.name}
        return self.render_to_response(context)


class AddTransactionView(PermissionMixin, View):
    permission_classes = (IsAuthenticated, )
    
    def post(self, request, room_id):
        room = Room.objects.get(id=room_id)

        if not room.is_owner(request.user):
            return _result_page(request, "You're not the owner of the room")
        
        amount = request.POST['amount']
        payer_id = request.POST['Payer']
        receiver_id = request.POST['Receiver']

        if payer_id == receiver_id:
            return _result_page(request, "ERROR: The payer and the receiver are the same")

        payer = Person.objects.get(id=payer_id)
        receiver = Person.objects.get(id=receiver_id)
        transaction = Transaction.objects.create(amount=amount, payer=payer, receiver=receiver)

        EmailGenerator.send_new_transaction_to_person(transaction)
        return redirect('ReportApp:home')


# TODO: use ListView
class TransactionListView(PermissionMixin, RawTemplateView):
    template_name = 'ReportApp/list_items/transaction.html'
    permission_classes = (IsAuthenticated, )
    
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)

        if not room.is_owner(request.user):
            return _result_page(request, "You're not the owner of the room")
    
        persons = room.person_set.all()
        payer_query = Q(payer__in=persons)
        receiver_query = Q(receiver__in=persons)
        transactions = Transaction.objects.filter(payer_query | receiver_query).order_by('-date')

        context = {'transactions': transactions, 'mode': 'transaction_log', 'room_name': room.name}
        return self.render_to_response(context)


# TODO: use ListView if possible
class RoomLogView(PermissionMixin, RawTemplateView):
    template_name = 'ReportApp/list_items/room_log.html'
    permission_classes = (IsAuthenticated, )
    
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)

        if not room.is_owner(request.user):
            return _result_page(request, "You're not the owner of the room")
        
        log = self._room_log_helper(room)

        context = {'log': log, 'mode': 'room_log', 'room_name': room.name}
        return self.render_to_response(context)


    def _room_log_helper(self, room):
        transactions = room.transaction_set
        spends = room.spend_set.all().order_by('-date')

        log = sorted(chain(transactions, spends),
                    key=lambda item: item.date,
                    reverse=True)
        return log


def _result_page(request, result):
    return render(request, 'result.html', context={'result': result})
