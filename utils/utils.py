import json


def pretty_print(d):
    p = json.dumps(d, sort_keys=True, indent=4)
    print(p)


def sort_dict_by_values(d, reverse=False):
    return {k: v for k, v in sorted(d.items(), key=lambda item: item[1][0], reverse=reverse)}
