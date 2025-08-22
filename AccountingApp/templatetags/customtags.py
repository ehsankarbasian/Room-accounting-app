from django import template
from AccountingApp.algorithm.core_algorithm import cleared_person


register = template.Library()


def set_cleared(person):
    person.cleared = cleared_person(person)
    person.save()


class CustomTag:
    def __init__(self, is_person_cleared):
        self.cleared_person = is_person_cleared
        self.set_cleared = set_cleared


@register.simple_tag
def call_function(method_name, *args):
    tag = CustomTag(cleared_person)
    method = getattr(tag, method_name)
    return method(*args)


@register.simple_tag
def callmethod(obj, method_name, *args, **kwargs):
    method = getattr(obj, method_name)
    return method(*args, **kwargs)
