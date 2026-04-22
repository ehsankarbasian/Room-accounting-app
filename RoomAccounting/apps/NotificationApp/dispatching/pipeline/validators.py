from dataclasses import is_dataclass

from ...interfaces import MessageDefinitionInterface


def ensure_valid_message_inputs(message_class, data):
    
    if not issubclass(message_class, MessageDefinitionInterface):
        raise TypeError(
            f"'{message_class.__name__}' must be a MessageDefinitionInterface implementation"
        )

    if not is_dataclass(data):
        raise TypeError(
            f"data must be a dataclass instance, got {type(data).__name__}"
        )

    expected_data_model = message_class.Data

    if not isinstance(data, expected_data_model):
        raise TypeError(
            f"{message_class} expects {expected_data_model.__name__} instance, "
            f"got {type(data).__name__}"
        )
