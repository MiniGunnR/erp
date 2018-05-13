from django.views.generic import ListView
import os, csv, shutil
from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.files import File

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from .forms import CreateUserForm, BaseProfileForm
from .models import Designation, Department, Mail


@login_required
def dashboard(request):
    return render(request, "core/dashboard.html")


def initial(request):
    europarts, created = Group.objects.get_or_create(name='Europarts')
    europarts_buyer, created = Group.objects.get_or_create(name='EuropartsBuyer')
    europarts_admin, created = Group.objects.get_or_create(name='EuropartsAdmin')

    view_cost_price = Permission.objects.get(codename='can_view_cost_price')
    add_cost_price = Permission.objects.get(codename='can_add_cost_price')
    edit_cost_price = Permission.objects.get(codename='can_edit_cost_price')

    view_selling_price = Permission.objects.get(codename='can_view_selling_price')
    add_selling_price = Permission.objects.get(codename='can_add_selling_price')
    edit_selling_price = Permission.objects.get(codename='can_edit_selling_price')

    add_product_list = Permission.objects.get(codename='can_add_product_list')

    europarts.permissions.add(view_selling_price)

    europarts_buyer.permissions.add(add_cost_price)
    europarts_buyer.permissions.add(edit_cost_price)

    europarts_admin.permissions.add(view_cost_price)
    europarts_admin.permissions.add(add_selling_price)
    europarts_admin.permissions.add(edit_selling_price)
    europarts_admin.permissions.add(add_product_list)

    return HttpResponse("OK")



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



from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


def create_bulk_user(request):
    with open(os.path.join(settings.BASE_DIR, 'media', 'core', 'employees.csv')) as f:
        reader = csv.reader(f)
        for row in reader:
            user, created = User.objects.get_or_create(
                username=str(row[0]),

                defaults={
                    'password': make_password('ddff123#'),
                    'first_name': ' '.join(row[1].split()[:-1]),
                    'last_name': str(row[1].split()[-1])
                }
            )
            designation, created = Designation.objects.get_or_create(
                name=str(row[4]), defaults={}
            )
            department, created = Department.objects.get_or_create(
                name=str(row[3])
            )
            user.profile.designation = designation
            user.profile.department = department
            user.profile.proximity_id = str(row[2])
            user.profile.save()

    context = {}
    return render(request, "core/create_bulk_user.html", context)


def db_backup(request):
    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    dbfile = File(open(db_path, "rb"))
    response = HttpResponse(dbfile, content_type='application/x-sqlite3')
    response['Content-Disposition'] = 'attachment; filename=%s' % db_path
    response['Content-Length'] = dbfile.size

    return response


class Mailbox(ListView):
    model = Mail
    paginate_by = 10
    template_name = 'core/mailbox.html'
    ordering = '-created'