from django.contrib import messages
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect

from .forms import ProductForm, ProductListForm

from .models import Product, ProductList


def home(request):
    return render(request, "europarts/home.html")


def create_product_request_list(request):
    ProductFormSet = formset_factory(ProductForm)

    if request.method == "POST":
        product_list_form = ProductListForm(request.POST)
        product_formset = ProductFormSet(request.POST)

        if product_list_form.is_valid() and product_formset.is_valid():

            ref_no = product_list_form.cleaned_data.get('ref_no')
            product_list = ProductList.objects.create(ref_no=ref_no)

            new_products = []

            for product_form in product_formset:
                description = product_form.cleaned_data.get('description')
                part_no = product_form.cleaned_data.get('part_no')
                brand = product_form.cleaned_data.get('brand')
                quantity = product_form.cleaned_data.get('quantity')
                unit = product_form.cleaned_data.get('unit')

                if description and part_no and quantity:
                    new_products.append(Product
                                        (product_list=product_list,
                                         description=description,
                                         part_no=part_no,
                                         brand=brand,
                                         quantity=quantity,
                                         unit=unit,
                                         ))
                try:
                    with transaction.atomic():
                        Product.objects.filter(product_list=product_list).delete()
                        Product.objects.bulk_create(new_products)

                        messages.success(request, 'Data saved!')
                        return HttpResponseRedirect(reverse('europarts:home'))
                except IntegrityError:
                    messages.error(request, 'There was an error saving your data.')
                    return HttpResponseRedirect(reverse('europarts:home'))
    else:
        product_list_form = ProductListForm()
        product_formset = ProductFormSet()

    context = {
        "product_list_form": product_list_form,
        "product_formset": product_formset,
    }
    return render(request, "europarts/create-product-request-list.html", context)

