
def send_email(subject, message, to_list, html_content):
    pass
    #message = EmailMultiAlternatives(subject,
    #                                 message,
    #                                 EMAIL_HOST_USER,
    #                                 to_list)
    #message.attach_alternative(html_content, "text/html")
    #message.send()


def send_text_email(subject, message, to_list):
    pass
    #for address in to_list:
    #    message = EmailMultiAlternatives(subject,
    #                                     message,
    #                                     EMAIL_HOST_USER,
    #                                     [address])
    #    message.send()
