import secrets


class VerificationTokenGenerator:

    MIN_VALUE = 100000
    MAX_VALUE = 999999

    @classmethod
    def generate(cls) -> str:
        number = secrets.randbelow(cls.MAX_VALUE - cls.MIN_VALUE + 1) + cls.MIN_VALUE
        return str(number)
