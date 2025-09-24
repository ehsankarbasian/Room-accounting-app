from itertools import chain

from apps.NotificationApp.core import NotificationFacade


class EmailGenerator:

    @staticmethod
    def send_new_spend_to_person(spend):
        subject = "New spend: '" + str(spend.amount) + "' FOR '" + spend.description + "'"
        message = EmailGenerator.__spend_message_creator(spend)

        for person in spend.room.person_set.all():
            related_person = bool(person in spend.related_persons)
            if person.verified_email and related_person:
                send_text_email(subject, message, [person.email])


    @staticmethod
    def __spend_message_creator(spend):
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


    @staticmethod
    def send_new_transaction_to_person(transaction):
        subject = "New transaction: '" + str(transaction.amount)\
                + "' FROM '" + transaction.payer.name\
                + "' TO '" + transaction.receiver.name + "'"
        message = EmailGenerator.__transaction_message_creator(transaction)

        if transaction.payer.verified_email:
            send_text_email(subject, message, [transaction.payer.email])
        if transaction.receiver.verified_email:
            send_text_email(subject, message, [transaction.receiver.email])


    @staticmethod
    def __transaction_message_creator(transaction):
        room = transaction.payer.room
        message = "the room admin fullname: " + room.creator.fullname + "\n" \
                + "room_name: '" + room.name + "'" + "\n" \
                + "admin email: " + room.creator.email + "\n" + "\n" \
                + "From:" + "\n" + "'" + transaction.payer.name + "'" + "\n" + "\n"\
                + "To:" + "\n" + "'" + transaction.receiver.name + "'"
        return message


    @staticmethod
    def send_room_log_email(person):
        subject = "Room log before you verify your email"
        log = EmailGenerator.__get_room_log_by_person(person)
        message = EmailGenerator.__room_log_message_creator(log)

        send_text_email(subject, message, [person.email])


    @staticmethod
    def __get_room_log_by_person(person):
        transactions = person.related_transactions
        spends = person.related_spends

        log = sorted(chain(transactions, spends),
                    key=lambda item: item.date,
                    reverse=True)
        return log


    @staticmethod
    def __room_log_message_creator(log):
        message = "Thanks you for verify your email" + "\n"\
                + "Your room records before you verify your email are as below:" + "\n" + "\n"

        for item in log:
            if item.is_transaction:
                date = str(item.date)
                message += "\n" + "'" + str(item.amount) + "' FROM '" + item.payer.name + "' TO '" + item.receiver.name\
                        + "' (date:" + date + ")\n"
            else:
                date = str(item.date)
                message += "\n" + "'" + str(item.amount) + "' FOR '" + item.description + "' (date:" + date + ")\n"
                message += "Spenders:" + "\n"
                for spender in item.spenders_set.all():
                    message += "\t" + spender.spender_person.name + " (w=" + str(spender.weight) + ")" + "\n"
                message += "Partners:" + "\n"
                for partner in item.partners_set.all():
                    message += "\t" + partner.partner_person.name + " (w=" + str(partner.weight) + ")" + "\n"
        return message
