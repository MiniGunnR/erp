import requests
import simplejson as json
from django.shortcuts import render


def home(request):
    payload = {'query': request.user.profile.sip}
    r = requests.get('http://172.16.16.172/php/billing.php', params=payload)
    d = json.loads(r.text)
    return render(request, "billing/home.html", { 'balance': d['balance'] })
