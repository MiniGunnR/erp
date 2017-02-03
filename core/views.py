from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .forms import CreateUserForm, BaseProfileForm


@login_required
def dashboard(request):
    return render(request, "core/dashboard.html")


def create_user(request):
    create_user_form = CreateUserForm(request.POST or None)
    profile_form = BaseProfileForm(request.POST or None)

    if create_user_form.is_valid():

        email = create_user_form.cleaned_data.get('username', None) + '@groupdesignace.com'
        return HttpResponse('email: {email}'.format(email=email))

    context = {
        "create_user_form": create_user_form,
        "profile_form": profile_form,
    }
    return render(request, "core/create_user.html", context)
