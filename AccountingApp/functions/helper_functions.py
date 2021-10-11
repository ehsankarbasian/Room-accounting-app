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
