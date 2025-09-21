import sys
import logging

from sms_ir import SmsIr as _SMS

import os
from dotenv import load_dotenv
load_dotenv()

sandbox_api_key = os.environ.get('SMS_SANDBOX_API_KEY')
# api_key = os.environ.get('SMS_API_KEY')
line_number = os.environ.get('SMS_LINE_NUMBER')


class _CustomSms(_SMS):
    
    def __init__(self, api_key, linenumber = None):
        super().__init__(api_key, linenumber)
    
    def config_logger(self):
        self.logger = logging.getLogger(__name__)
        if self.logger.hasHandlers():
            return
        
        self.log_level=logging.INFO
        log_format = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s')
        self.logger.setLevel(self.log_level)

        # writing to stdout
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(self.log_level)
        handler.setFormatter(log_format)
        self.logger.addHandler(handler)


sms_ir = _CustomSms(f'{sandbox_api_key}a', line_number)
sms_ir = _CustomSms(sandbox_api_key, line_number)
# sms_ir = _CustomSms(api_key, line_number)


def send_text_sms(message, to, line_number=line_number):
    sms_ir.send_sms(number=to, message=message, linenumber=line_number)


if __name__ == "__main__":
    send_text_sms(to=9376265623, message='__MESSAGE__')
