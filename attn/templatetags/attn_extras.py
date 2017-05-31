from django import template
import calendar

register = template.Library()

@register.filter
def month_name(month_number):
    return calendar.month_name[month_number]

@register.filter
def present(dict, key):
    return dict[key][0]


@register.filter
def late(dict, key):
    return dict[key][1]


@register.filter
def absent(dict, key):
    return dict[key][2]


@register.filter
def check_if_late(time_str):
    if ':' in time_str:
        hour = int(time_str[:2])
        minute = int(time_str[-2:])
        print(hour, minute)
        if (hour < 9) or (hour == 9 and minute <= 30):
            response = 'success'
        elif (hour > 9) or (hour == 9 and minute > 30):
            response = 'warning'
        else:
            response = 'danger'
    else:
        response = 'danger'
    return response
