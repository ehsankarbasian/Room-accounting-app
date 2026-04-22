from typing import List

from ....registry import SenderRegistry
from ....interfaces import MessageSenderInterface


def build_sender_chain(delivery_options, primary_resolved_channel):
    
    # Build the primary delivery channel based on the recipient's resolved notification method
    sender_classes: List[type[MessageSenderInterface]] = []
    primary_sender_class = SenderRegistry.get(primary_resolved_channel.channel_type)
    sender_classes.append(primary_sender_class)

    # Append fallback sender classes provided by delivery options for alternative delivery paths
    fallback_channels: List[type[MessageSenderInterface]] = []
    if delivery_options.fallback_channels:
        fallback_channels = delivery_options.fallback_channels
    sender_classes.extend(fallback_channels)
    
    return sender_classes
