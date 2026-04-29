
class ChannelServiceException(Exception):
    pass


class ChannelAlreadyExists(ChannelServiceException):
    pass


class UnsupportedChannelType(ChannelServiceException):
    pass


class ChannelNotFound(ChannelServiceException):
    pass
