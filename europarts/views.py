from django.contrib import messages
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import ListView
from utils.func import is_member
from django.contrib.auth.decorators import login_required

from .forms import ProductForm, ListForm

from .models import Product, List, CarPart


def home(request):
    return render(request, "europarts/home.html")


class ProductRequestListView(ListView):
    model = List
    template_name = "europarts/product-request-list.html"

    def get_queryset(self):
        if is_member(self.request.user, 'Europarts'):
            return List.objects.filter(selling_price_quoted=True)
        return List.objects.all()


def create_product_request_list(request):

    ProductFormSet = formset_factory(ProductForm)

    if request.method == "POST":
        list_form = ListForm(request.POST)
        product_formset = ProductFormSet(request.POST)

        if list_form.is_valid() and product_formset.is_valid():
            ref_no = list_form.cleaned_data.get('ref_no')
            list_obj = List.objects.create(ref_no=ref_no)

            new_products = []

            for product_form in product_formset:
                description = product_form.cleaned_data.get('description')
                part_no = product_form.cleaned_data.get('part_no')
                brand = product_form.cleaned_data.get('brand')
                quantity = product_form.cleaned_data.get('quantity')
                unit = product_form.cleaned_data.get('unit')

                car_part, created = CarPart.objects.get_or_create(part_no=part_no, description=description, brand=brand, defaults={})
                product_obj = new_products.append(Product(product_list=list_obj,
                                                          car_part=car_part,
                                                          quantity=quantity,
                                                          unit=unit))

            try:
                Product.objects.bulk_create(new_products)

                messages.success(request, 'Data saved!')
                return HttpResponseRedirect(reverse('europarts:home'))
            except IntegrityError:
                messages.error(request, 'There was an error saving your data.')
                return HttpResponseRedirect(reverse('europarts:home'))

    else:
        list_form = ListForm()
        product_formset = ProductFormSet()

    print(product_formset.errors)

    context = {
        "list_form": list_form,
        "product_formset": product_formset,
    }

    return render(request, "europarts/create-product-request-list.html", context)


@login_required
def edit_product_request_list(request, pk):
    ProductFormSet = formset_factory(ProductForm, extra=0)

    list_obj = List.objects.get(id=pk)

    old_products = Product.objects.filter(product_list=list_obj)
    product_data = [
        {'description': product.car_part.description,
         'part_no': product.car_part.part_no,
         'brand': product.car_part.brand,
         'quantity': product.quantity,
         'unit': product.unit,
         'cost_price': product.cost_price,
         'selling_price': product.selling_price,}

        for product in old_products
        ]

    if request.method == "POST":
        product_formset = ProductFormSet(request.POST)

        if product_formset.is_valid():

            Product.objects.filter(product_list=list_obj).delete()

            for product_form in product_formset:
                description = product_form.cleaned_data.get('description')
                part_no = product_form.cleaned_data.get('part_no')
                brand = product_form.cleaned_data.get('brand')
                quantity = product_form.cleaned_data.get('quantity')
                unit = product_form.cleaned_data.get('unit')
                cost_price = product_form.cleaned_data.get('cost_price')
                selling_price = product_form.cleaned_data.get('selling_price')

                car_part, created = CarPart.objects.get_or_create(part_no=part_no, description=description, brand=brand, defaults={})
                product = Product.objects.create(product_list=list_obj,
                                                 car_part=car_part,
                                                 quantity=quantity,
                                                 unit=unit,
                                                 cost_price=cost_price,
                                                 selling_price=selling_price)

            if request.user.has_perm('europarts.can_add_cost_price'):
                list_obj.cost_price_quoted = True
                list_obj.save()

            if request.user.has_perm('europarts.can_add_selling_price') and list_obj.cost_price_quoted:
                list_obj.selling_price_quoted = True
                list_obj.save()

            return HttpResponseRedirect(reverse('europarts:home'))

    else:
        product_formset = ProductFormSet(initial=product_data)

    context = {
        "list_obj": list_obj,
        "product_formset": product_formset,
    }
    return render(request, "europarts/edit-product-request-list.html", context)


def get_part_info(request, part_no):
    try:
        car_part = CarPart.objects.get(part_no=part_no)
    except CarPart.DoesNotExist:
        return JsonResponse({"description": "", "brand": ""})
    else:
        return JsonResponse({"description": car_part.description, "brand": car_part.brand})
