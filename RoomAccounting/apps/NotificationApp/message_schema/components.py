from dataclasses import dataclass


@dataclass
class Button:
    """
    Interactive button that may appear in supported channels
    """

    text: str
    target: str


@dataclass
class ButtonLink(Button):
    pass
