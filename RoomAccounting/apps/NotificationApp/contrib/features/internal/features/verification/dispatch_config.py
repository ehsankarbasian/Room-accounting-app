from .message import VerifyChannelMessage

from ......dispatching.options import ChannelSelectionOptions

from ......registry import MessageOptionsRegistry
from ......interfaces import MessageSenderInterface


def register_verify_message_options_for_channel(channel: MessageSenderInterface):
    
    MessageOptionsRegistry.set(
        VerifyChannelMessage,
        channel_selection_options=ChannelSelectionOptions(
            channel_override=channel,
            require_verified=False
        )
    )
