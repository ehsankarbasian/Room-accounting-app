import secrets

from .interface import TokenGeneratorInterface


class NumericSixDigitTokenGenerator(TokenGeneratorInterface):
    
    @staticmethod
    def generate() -> str:
        MIN_VALUE = 100000
        MAX_VALUE = 999999
        
        number = secrets.randbelow(MAX_VALUE - MIN_VALUE + 1) + MIN_VALUE
        return str(number)
