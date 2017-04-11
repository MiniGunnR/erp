import requests
import simplejson as json
from django.shortcuts import render


def home(request):
    payload = { 'query': request.user.profile.sip }
    r = requests.get('http://172.16.16.172/php/billing.php', params=payload)
    d = json.loads(r.text)
    context = {
        "balance": d['balance'],
    }
    return render(request, "billing/home.html", context)


def check_employee_balance(request):
    sip = request.GET.get('sip', request.user.profile.sip)
    payload = { 'query': sip }
    r = requests.get('http://172.16.16.172/php/billing.php', params=payload)
    d = json.loads(r.text)
    context = {
        "balance": d['balance'],
    }
    return render(request, "billing/check_employee_balance.html", context)


def billing_list(request):
    r = request.get('http://172.16.16.172/php/billing_list.php')
    d = json.loads(r.text)
    context = {
        "d": d,
    }
    return render(request, "billing/billing_list.html", context)
