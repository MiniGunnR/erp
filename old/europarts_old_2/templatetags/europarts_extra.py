from django import template
from ..models import AutoPart

register = template.Library()


@register.filter
def fetch_auto_part_details(auto_part_id):
    obj = AutoPart.objects.get(id=auto_part_id)
    return obj


@register.filter
def ternary(logic, values):
    value_list = values.split(",")
    if logic:
        return value_list[0]
    else:
        return value_list[1]
