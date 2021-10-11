from itertools import chain
from secrets import token_hex
from random import randint

from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from RoomAccounting.settings import HOST, PORT, ROOM_ACCOUNTING_APP_BASE_URL, EMAIL_HOST_USER


def landing_page(request):
    if not request.user.is_anonymous:
        return home(request)

    context = {'HOST': HOST, 'PORT': PORT}
    return render(request, 'index.html', context=context)


def home(request):
    user = request.user
    rooms = Room.objects.filter(creator=user).order_by("-created_at")
    context = {'HOST': HOST, 'PORT': PORT, 'username': user.username, 'rooms': rooms}
    return render(request, 'home.html', context=context)


def send_email(subject, message, to_list, html_content):
    message = EmailMultiAlternatives(subject,
                                     message,
                                     EMAIL_HOST_USER,
                                     to_list)
    message.attach_alternative(html_content, "text/html")
    message.send()


def send_text_email(subject, message, to_list):
    for address in to_list:
        message = EmailMultiAlternatives(subject,
                                         message,
                                         EMAIL_HOST_USER,
                                         [address])
        message.send()


@require_http_methods(["POST"])
def sign_up(request):
    fullname = request.POST['fullname']
    phone_number = request.POST['phone_number']
    email = request.POST['email']
    username = request.POST['username']
    password = request.POST['password']

    verify_email_token = token_hex(64)
    token = Token.objects.create(verify_email_token=verify_email_token,
                                 verify_email_code=randint(100000, 999999),
                                 reset_pass_token=token_hex(64),
                                 reset_pass_code=randint(100000, 999999))

    User.objects.create_user(username=username,
                             password=password,
                             email=email,
                             phone_number=phone_number,
                             fullname=fullname,
                             token=token)

    message = "Hello " + fullname + ". please click on the button below to verify your email"
    html_content = get_template('email_verification.html').render(context={'HOST': HOST,
                                                                           'PORT': PORT,
                                                                           'email': email,
                                                                           'name': username,
                                                                           'app_base_url': ROOM_ACCOUNTING_APP_BASE_URL,
                                                                           'verify_email_token': verify_email_token})
    send_email("Verify email", message, [email], html_content)

    return HttpResponse("Signed up successfully,"
                        + " now verify at least one of your email or phone number and then sign in please")


@api_view(['POST'])
def verify_email(request):
    token = request.POST['token']
    email = request.POST['email']

    user = User.objects.filter(email=email)
    if user.count() == 0:
        return HttpResponse("User not found")

    user = user[0]
    if user.verified_email:
        return HttpResponse("Your email verified before")

    if token != user.token.verify_email_token:
        return HttpResponse("Wrong token")

    user.verified_email = True
    user.save()
    return HttpResponse("Email verified successfully. you can sign in.")


def forgot_password(request):
    email = request.GET['email']

    user = User.objects.filter(email=email)
    if user.count() == 0:
        return HttpResponse("User not found")

    user = user[0]
    reset_password_token = user.token.reset_pass_token

    html_content = get_template('reset_password.html').render(context={
        'HOST': HOST,
        'PORT': PORT,
        'app_base_url': ROOM_ACCOUNTING_APP_BASE_URL,
        'email': email,
        'name': user.fullname,
        'token': reset_password_token})
    send_email(subject='reset password',
               message='message',
               to_list=[email],
               html_content=html_content)

    return HttpResponse("Email sent")


@api_view(['POST'])
def reset_password_token_based(request):
    token = request.POST['token']
    email = request.POST['email']
    password_1 = request.POST['password_1']
    password_2 = request.POST['password_2']

    user = User.objects.filter(email=email)
    if user.count() == 0:
        return HttpResponse("User not found")

    if password_1 != password_2:
        return HttpResponse("the passwords are not equal")

    user = user[0]
    if not user.verified_email:
        return HttpResponse("Your email is not verified")

    if user.token.reset_pass_token != token:
        print(user.token.reset_pass_token)
        print(token)
        return HttpResponse("Wrong token")

    user.set_password(password_1)
    user.token.reset_pass_token = token_hex(64)
    user.save()
    return HttpResponse("Password changed successfully. you can sign in.")


@require_http_methods(["POST"])
def sign_in(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is None:
        return HttpResponse('Wrong username/password')

    if not (user.verified_email or user.verified_phone):
        return HttpResponse("Verify at least one of your email or phone number to sign in")

    login(request, user)
    return redirect('home')


def log_out(request):
    logout(request)
    return redirect('landing_page')


def add_room(request):
    room_name = request.GET['room_name']

    if request.user.is_authenticated:
        Room.objects.create(name=room_name, creator=request.user)
        return redirect('home')
    return HttpResponse('Please signIn')


def delete_room(request, room_id):
    if request.user.is_anonymous:
        return HttpResponse("Please sign in")

    room = Room.objects.get(id=room_id)

    if room in request.user.room_set.all():
        room.delete()
        return redirect('home')
    return HttpResponse("You're not the owner of the room")


@require_http_methods(["POST"])
def edit_room(request, room_id):
    if request.user.is_anonymous:
        return HttpResponse("Please sign in")

    room = Room.objects.get(id=room_id)

    if room in request.user.room_set.all():
        room.name = request.POST['room_name']
        room.save()
        return redirect('home')
    return HttpResponse("You're not the owner of the room")


@require_http_methods(["POST"])
def add_person(request, room_id):
    if request.user.is_anonymous:
        return HttpResponse("Please sign in")

    room = Room.objects.get(id=room_id)

    if room in request.user.room_set.all():
        name = request.POST['person_name']
        email = request.POST['email']
        phone = request.POST['phone']
        Person.objects.create(name=name, email=email, phone=phone, room=room)
        return redirect('home')
    return HttpResponse("You're not the owner of the room")


@require_http_methods(["POST"])
def add_buy(request, room_id):
    if request.user.is_anonymous:
        return HttpResponse("Please sign in")

    room = Room.objects.get(id=room_id)

    if room in request.user.room_set.all():
        amount = request.POST['amount']
        description = request.POST['description']
        spend = Spend.objects.create(amount=amount, description=description, room=room)

        # m2m relationships:
        for person in room.person_set.all():
            # Create Spenders
            ID = str(person.id)
            if "spender"+ID in request.POST:
                # TODO: det and save weight
                Spenders.objects.create(spender_person=person, spender_spend=spend)

            # Create Partners
            if "partner"+ID in request.POST:
                # TODO: det and save weight
                Partners.objects.create(partner_person=person, partner_spend=spend)

        return redirect('home')

    return HttpResponse("You're not the owner of the room")


def all_buys(request, room_id):
    if request.user.is_anonymous:
        return HttpResponse("Please sign in")

    room = Room.objects.get(id=room_id)
    if room in request.user.room_set.all():
        spends = room.spend_set.all().order_by('-date')

        context = {'spends': spends, 'mode': 'spend_log', 'room_name': room.name}
        return render(request, 'log.html', context=context)

    return HttpResponse("You're not the owner of the room")


@require_http_methods(["POST"])
def add_transaction(request, room_id):
    if request.user.is_anonymous:
        return HttpResponse("Please sign in")

    room = Room.objects.get(id=room_id)

    if room in request.user.room_set.all():
        amount = request.POST['amount']
        payer_id = request.POST['Payer']
        receiver_id = request.POST['Receiver']

        if payer_id == receiver_id:
            return HttpResponse('ERROR: The payer and the receiver are the same')

        payer = Person.objects.get(id=payer_id)
        receiver = Person.objects.get(id=receiver_id)
        Transaction.objects.create(amount=amount, payer=payer, receiver=receiver)
        return redirect('home')

    return HttpResponse("You're not the owner of the room")


def all_transactions(request, room_id):
    if request.user.is_anonymous:
        return HttpResponse("Please sign in")

    room = Room.objects.get(id=room_id)

    if room in request.user.room_set.all():
        persons = room.person_set.all()
        payer_query = Q(payer__in=persons)
        receiver_query = Q(receiver__in=persons)
        transactions = Transaction.objects.filter(payer_query | receiver_query).order_by('-date')

        context = {'transactions': transactions, 'mode': 'transaction_log', 'room_name': room.name}
        return render(request, 'log.html', context=context)

    return HttpResponse("You're not the owner of the room")


def room_log(request, room_id):
    if request.user.is_anonymous:
        return HttpResponse("Please sign in")

    room = Room.objects.get(id=room_id)

    if room in request.user.room_set.all():
        transactions = room.transaction_set
        spends = room.spend_set.all().order_by('-date')

        log = sorted(chain(transactions, spends),
                     key=lambda item: item.date,
                     reverse=True)

        context = {'log': log, 'mode': 'room_log', 'room_name': room.name}
        return render(request, 'log.html', context=context)

    return HttpResponse("You're not the owner of the room")


def report_for_clearing(request, room_id):
    if request.user.is_anonymous:
        return HttpResponse("Please sign in")

    room = Room.objects.get(id=room_id)
    if room not in request.user.room_set.all():
        return HttpResponse("You're not the owner of the room")

    # The core algorithm:
    final_dict = calculate_result(room)

    context = {'result': final_dict, 'mode': 'report_for_clearing', 'room_name': room.name}
    return render(request, 'log.html', context=context)


@api_view(['POST'])
def report_for_clearing_API(request):
    room_id = request.data['room_id']
    room = Room.objects.get(id=room_id)

    final_dict = calculate_result(room)
    final_dict = simple_result(final_dict)

    return Response(final_dict, status=status.HTTP_200_OK)


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
