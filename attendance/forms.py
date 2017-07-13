from django import forms
from django.utils.dates import MONTHS
from datetime import datetime


class OffDayName(forms.Form):
    details = forms.CharField()


class OffDayFrom(forms.Form):
    from_year = forms.ChoiceField(label="Year", choices=[(x, x) for x in range(2017, (datetime.now().year + 2))])
    from_month = forms.ChoiceField(label="Month", choices=[(num, name) for num, name in MONTHS.items()])
    from_date = forms.ChoiceField(label="Day", choices=[(x, x) for x in range(1, 32)])


class OffDayTo(forms.Form):
    to_year = forms.ChoiceField(label="Year", choices=[(x, x) for x in range(2017, (datetime.now().year + 2))])
    to_month = forms.ChoiceField(label="Month", choices=[(num, name) for num, name in MONTHS.items()])
    to_date = forms.ChoiceField(label="Day", choices=[(x, x) for x in range(1, 32)])


class LeaveType(forms.Form):
    type = forms.ChoiceField(label="Type", choices=[('S', 'Sick'), ('C', 'Casual')])


class LeaveFrom(forms.Form):
    from_year = forms.ChoiceField(label="Year", choices=[(x, x) for x in range(2017, (datetime.now().year + 2))])
    from_month = forms.ChoiceField(label="Month", choices=[(num, name) for num, name in MONTHS.items()])
    from_date = forms.ChoiceField(label="Day", choices=[(x, x) for x in range(1, 32)])


class LeaveTo(forms.Form):
    to_year = forms.ChoiceField(label="Year", choices=[(x, x) for x in range(2017, (datetime.now().year + 2))])
    to_month = forms.ChoiceField(label="Month", choices=[(num, name) for num, name in MONTHS.items()])
    to_date = forms.ChoiceField(label="Day", choices=[(x, x) for x in range(1, 32)])

