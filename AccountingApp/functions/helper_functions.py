from django.core.mail import EmailMultiAlternatives
from RoomAccounting.settings import EMAIL_HOST_USER

from django.test import Client
from django.shortcuts import render
from RoomAccounting.settings import ROOM_ACCOUNTING_APP_BASE_URL


def result_page(request, result):
    return render(request, 'result.html', context={'result': result})


def client_post(url, json):
    response = Client().post("/" + ROOM_ACCOUNTING_APP_BASE_URL + "/" + url, json, format='json')
    return response.data


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


def send_new_spend_to_person(spend):
    subject = "New spend: '" + str(spend.amount) + "' FOR '" + spend.description + "'"
    message = spend_message_creator(spend)

    for person in spend.room.person_set.all():
        related_person = bool(person in spend.related_persons)
        if person.verified_email and related_person:
            send_text_email(subject, message, [person.email])


def spend_message_creator(spend):
    creator = spend.room.creator
    message = "the room admin fullname: " + creator.fullname + "\n" \
              + "room_name: '" + spend.room.name + "'" + "\n" \
              + "admin email: " + creator.email + "\n" + "\n" \
              + "Spenders:" + "\n"

    for spender in spend.spenders_set.all():
        message += spender.spender_person.name + " (weight=" + str(spender.weight) + ")" + "\n"
    message += "\n" + "Partners: " + "\n"
    for partner in spend.partners_set.all():
        message += partner.partner_person.name + " (weight=" + str(partner.weight) + ")" + "\n"

    return message


def send_new_transaction_to_person(transaction):
    subject = "New transaction: '" + str(transaction.amount)\
              + "' FROM '" + transaction.payer.name\
              + "' TO '" + transaction.receiver.name + "'"
    message = transaction_message_creator(transaction)

    if transaction.payer.verified_email:
        send_text_email(subject, message, [transaction.payer.email])
    if transaction.receiver.verified_email:
        send_text_email(subject, message, [transaction.receiver.email])


def transaction_message_creator(transaction):
    room = transaction.payer.room
    message = "the room admin fullname: " + room.creator.fullname + "\n" \
              + "room_name: '" + room.name + "'" + "\n" \
              + "admin email: " + room.creator.email + "\n" + "\n" \
              + "From:" + "\n" + "'" + transaction.payer.name + "'" + "\n" + "\n"\
              + "To:" + "\n" + "'" + transaction.receiver.name + "'"
    return message
