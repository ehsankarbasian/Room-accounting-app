from sms_ir import SmsIr

import os
from dotenv import load_dotenv
load_dotenv()

sandbox_api_key = os.environ.get('SMS_SANDBOX_API_KEY')
# api_key = os.environ.get('SMS_API_KEY')
line_number = os.environ.get('SMS_LINE_NUMBER')


sms_ir = SmsIr(f'{sandbox_api_key}a', line_number)
sms_ir = SmsIr(sandbox_api_key, line_number)
# sms_ir = SmsIr(api_key, line_number)


def send_text_sms(message, to, line_number=line_number):
    sms_ir.send_sms(number=to, message=message, linenumber=line_number)


# How to use
send_text_sms(to=9376265623, message='__MESSAGE__')
