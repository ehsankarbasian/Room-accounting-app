from django.views.generic.base import View
from django.shortcuts import redirect, get_object_or_404

from apps.ReportApp.models import Spend, Room, Spenders, Partners

from apps.AuthApp.persmissions.mixins import PermissionMixin
from apps.AuthApp.persmissions.permissions import IsAuthenticated


class AddSpendView(PermissionMixin, View):
    permission_classes = (IsAuthenticated, )
    
    def post(self, request, room_id):
        room = get_object_or_404(Room, id=room_id, creator__id=request.user.id)
        
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
        
        # TODO:
        # EmailGenerator.send_new_spend_to_person(spend)
        
        return redirect('ReportApp:home')
