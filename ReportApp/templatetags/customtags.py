from django import template

from ReportApp.models import Person
from ReportApp.algorithm import ReportFacade


register = template.Library()


def cleared_person(person):
    graph = ReportFacade.get_graph(person.room)
    for k, j in graph.edges():
        weight = graph.get_edge_weight(k, j)
        if weight != 0 and person.id in [k, j]:
            return True
    return False


def set_cleared(person):
    person.cleared = cleared_person(person)
    person.save()


@register.simple_tag
def get_person_name_by_id(id_):
    return Person.objects.get(id=id_).name


class CustomTag:
    def __init__(self):
        self.cleared_person = cleared_person
        self.set_cleared = set_cleared


@register.simple_tag
def call_function(method_name, *args):
    tag = CustomTag()
    method = getattr(tag, method_name)
    return method(*args)


@register.simple_tag
def callmethod(obj, method_name, *args, **kwargs):
    method = getattr(obj, method_name)
    return method(*args, **kwargs)


@register.simple_tag
def copy_name(obj):
    return obj
