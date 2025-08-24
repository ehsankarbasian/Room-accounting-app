from secrets import token_hex
from itertools import chain
from random import randint

from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.views.generic.base import View

from ReportApp.models import Room, Person, Spend, Spenders, Partners, Transaction
from django.db.models import Q
from utils.email import send_email
from utils.custon_views.views import RawTemplateView
from ReportApp.email_generator import EmailGenerator
from RoomAccounting.settings import HOST, PORT, ROOM_ACCOUNTING_APP_BASE_URL


# TODO: Use ModelViews to CRUD


class AddRoomView(View):
    
    def post(self, request):
        room_name = request.POST['room_name']

        if request.user.is_authenticated:
            Room.objects.create(name=room_name, creator=request.user)
            return redirect('home')
        return _result_page(request, "Please sign in.")


class DeleteRoomView(View):
    
    def post(self, request, room_id):
        if request.user.is_anonymous:
            return _result_page(request, "Please sign in")

        room = Room.objects.get(id=room_id)

        if room in request.user.room_set.all():
            # TODO: 2 factor auth to delete the room
            # room.delete()
            return redirect('home')
        return _result_page(request, "You're not the owner of the room")


class EditRoomView(View):
    
    def post(self, request, room_id):
        if request.user.is_anonymous:
            return _result_page(request, "Please sign in")

        room = Room.objects.get(id=room_id)

        if room in request.user.room_set.all():
            room.name = request.POST['room_name']
            room.save()
            return redirect('home')
        return _result_page(request, "You're not the owner of the room")


class AddPersonView(View):
    
    def post(self, request, room_id):
        if request.user.is_anonymous:
            return _result_page(request, "Please sign in")

        room = Room.objects.get(id=room_id)

        if room in request.user.room_set.all():
            name = request.POST['person_name']
            email = request.POST['email']
            phone = request.POST['phone']
            person = Person.objects.create(name=name, email=email, phone=phone, room=room,
                                        verify_email_token=token_hex(64), verify_phone_code=randint(100000, 999999))

            context = {'HOST': HOST,
                    'PORT': PORT,
                    'person_id': person.id,
                    'name': name,
                    'mode': 'verifyPersonEmail',
                    'app_base_url': ROOM_ACCOUNTING_APP_BASE_URL,
                    'verify_email_token': person.verify_email_token}
            html_content = get_template('email_verification.html').render(context=context)

            message = "Hello " + name + ". please click on the button below to verify your email"
            send_email("Verify email", message, [email], html_content)

            return redirect('home')

        return _result_page(request, "You're not the owner of the room")


class AddSpendView(View):
    
    def post(self, request, room_id):
        if request.user.is_anonymous:
            return _result_page(request, "Please sign in")

        room = Room.objects.get(id=room_id)

        if room in request.user.room_set.all():
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
            return redirect('home')

        return _result_page(request, "You're not the owner of the room")


# TODO: use ListView
class SpendListView(RawTemplateView):
    template_name = 'list_items/spend.html'
    
    def get(self, request, room_id):
        if request.user.is_anonymous:
            return _result_page(request, "Please sign in")

        room = Room.objects.get(id=room_id)
        if room in request.user.room_set.all():
            spends = room.spend_set.all().order_by('-date')

            context = {'spends': spends, 'mode': 'spend_log', 'room_name': room.name}
            return self.render_to_response(context)

        return _result_page(request, "You're not the owner of the room")


class AddTransactionView(View):
    
    def post(self, request, room_id):
        if request.user.is_anonymous:
            return _result_page(request, "Please sign in")

        room = Room.objects.get(id=room_id)

        if room in request.user.room_set.all():
            amount = request.POST['amount']
            payer_id = request.POST['Payer']
            receiver_id = request.POST['Receiver']

            if payer_id == receiver_id:
                return _result_page(request, "ERROR: The payer and the receiver are the same")

            payer = Person.objects.get(id=payer_id)
            receiver = Person.objects.get(id=receiver_id)
            transaction = Transaction.objects.create(amount=amount, payer=payer, receiver=receiver)

            EmailGenerator.send_new_transaction_to_person(transaction)
            return redirect('home')

        return _result_page(request, "You're not the owner of the room")


# TODO: use ListView
class TransactionListView(RawTemplateView):
    template_name = 'list_items/transaction.html'
    
    def get(self, request, room_id):
        if request.user.is_anonymous:
            return _result_page(request, "Please sign in")

        room = Room.objects.get(id=room_id)

        if room in request.user.room_set.all():
            persons = room.person_set.all()
            payer_query = Q(payer__in=persons)
            receiver_query = Q(receiver__in=persons)
            transactions = Transaction.objects.filter(payer_query | receiver_query).order_by('-date')

            context = {'transactions': transactions, 'mode': 'transaction_log', 'room_name': room.name}
            return self.render_to_response(context)

        return _result_page(request, "You're not the owner of the room")
    

# TODO: use ListView if possible
class RoomLogView(RawTemplateView):
    template_name = 'list_items/room_log.html'
    
    def get(self, request, room_id):
        if request.user.is_anonymous:
            return _result_page(request, "Please sign in")

        room = Room.objects.get(id=room_id)

        if room in request.user.room_set.all():
            log = self._room_log_helper(room)

            context = {'log': log, 'mode': 'room_log', 'room_name': room.name}
            return self.render_to_response(context)

        return _result_page(request, "You're not the owner of the room")


    def _room_log_helper(self, room):
        transactions = room.transaction_set
        spends = room.spend_set.all().order_by('-date')

        log = sorted(chain(transactions, spends),
                    key=lambda item: item.date,
                    reverse=True)
        return log


def _result_page(request, result):
    return render(request, 'result.html', context={'result': result})
