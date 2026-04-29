
class ChannelServiceException(Exception):
    pass


class ChannelAlreadyExists(ChannelServiceException):
    pass


class UnsupportedChannelType(ChannelServiceException):
    pass


class ChannelNotFound(ChannelServiceException):
    pass


class ChannelAlreadyVerified(ChannelServiceException):
    pass


class InvalidVerificationToken(ChannelServiceException):
    pass


class VerificationTokenExpired(ChannelServiceException):
    pass

