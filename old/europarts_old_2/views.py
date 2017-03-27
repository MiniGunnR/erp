import uuid

from django.contrib import messages
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, Http404
from django.views import generic
from django.core.cache import cache
from num2words import num2words

from datetime import datetime

from .models import Brand, AutoType, AutoPart, List, Product, Quotation, QuotationProduct, QuotationCode

from .forms import ProductCreateForm, ListForm, AddCostPriceForm, AddSellingPriceForm


def home(request):
    return render(request, "europarts/home.html")


def create_product_request_list(request):

    ProductFormSet = formset_factory(ProductCreateForm)

    if request.method == "POST":
        list_form = ListForm(request.POST)
        product_formset = ProductFormSet(request.POST)
        print(request.POST)

        if list_form.is_valid() and product_formset.is_valid():
            ref_no = list_form.cleaned_data.get('ref_no')
            list_obj = List.objects.create(ref_no=ref_no)

            new_products = []

            for product_form in product_formset:
                brand = product_form.cleaned_data.get('brand')
                # print(brand_id)
                # brand = Brand.objects.get(id=brand_id)

                auto_type = product_form.cleaned_data.get('auto_type')
                # auto_type = AutoType.objects.get(id=auto_type_id)

                description = product_form.cleaned_data.get('description')
                part_no = product_form.cleaned_data.get('part_no')
                quantity = product_form.cleaned_data.get('quantity')
                unit = product_form.cleaned_data.get('unit')

                print(request.POST)
                auto_part, created = AutoPart.objects.get_or_create(brand=brand, auto_type=auto_type, part_no=part_no, description=description, defaults={})
                product_obj = new_products.append(Product(product_list=list_obj,
                                                          auto_part=auto_part,
                                                          quantity=quantity,
                                                          unit=unit))

            try:
                Product.objects.bulk_create(new_products)

                messages.success(request, 'Data saved!')
                return HttpResponseRedirect(reverse('europarts_old_2:home'))
            except IntegrityError:
                messages.error(request, 'There was an error saving your data.')
                return HttpResponseRedirect(reverse('europarts_old_2:home'))

    else:
        list_form = ListForm()
        product_formset = ProductFormSet()

    context = {
        "list_form": list_form,
        "product_formset": product_formset,
    }

    return render(request, "europarts/create-product-request-list.html", context)


class ProductRequestListView(generic.ListView):
    model = List
    template_name = "europarts/product-request-listview.html"
    context_object_name = 'lists'


class ProductRequestDetailView(generic.DetailView):
    model = List
    template_name = "europarts/product-request-detailview.html"

    def get_context_data(self, **kwargs):
        context = super(ProductRequestDetailView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.filter(product_list=self.object)
        return context


def add_cost_price(request, pk):
    product_list = List.objects.get(id=pk)
    AddCostPriceFormset = formset_factory(AddCostPriceForm, extra=0)

    product_objs = Product.objects.filter(product_list=product_list)
    product_data = [{"auto_part": product.auto_part, "cost_price": product.cost_price} for product in product_objs]

    if request.method == "POST":
        add_cost_formset = AddCostPriceFormset(request.POST)

        if add_cost_formset.is_valid():

            for form in add_cost_formset:
                cost_price = form.cleaned_data.get('cost_price')
                auto_part = form.cleaned_data.get('auto_part')

                obj = Product.objects.get(product_list=product_list, auto_part=auto_part)
                obj.cost_price = cost_price
                obj.save()

            if not product_list.cost_price_quoted:
                product_list.cost_price_quoted = True
                product_list.save()

            return HttpResponseRedirect(reverse('europarts_old_2:product-request-detail', args=(pk,)))

    else:
        add_cost_formset = AddCostPriceFormset(initial=product_data)
    context = {
        "product_list": product_list,
        "add_cost_formset": add_cost_formset,
    }
    return render(request, "europarts/add-cost-price.html", context)


def add_selling_price(request, pk):
    product_list = List.objects.get(id=pk)
    AddSellingPriceFormset = formset_factory(AddSellingPriceForm, extra=0)

    product_objs = Product.objects.filter(product_list=product_list)
    product_data = [{"auto_part": product.auto_part, "cost_price": product.cost_price, "selling_price": product.selling_price} for product in product_objs]

    if request.method == "POST":
        add_sp_formset = AddSellingPriceFormset(request.POST)

        if add_sp_formset.is_valid():

            for form in add_sp_formset:
                selling_price = form.cleaned_data.get('selling_price')
                auto_part = form.cleaned_data.get('auto_part')

                obj = Product.objects.get(product_list=product_list, auto_part=auto_part)
                obj.selling_price = selling_price
                obj.save()

            if not product_list.selling_price_quoted:
                product_list.selling_price_quoted = True
                product_list.save()

            return HttpResponseRedirect(reverse('europarts_old_2:product-request-detail', args=(pk,)))
    else:
        add_sp_formset = AddSellingPriceFormset(initial=product_data)

    context = {
        "product_list": product_list,
        "add_sp_formset": add_sp_formset,
    }
    return render(request, "europarts/add-selling-price.html", context)


def create_quotation(request):
    if request.method == 'POST':
        recipient = request.POST.get('recipient')
        recipient_address = request.POST.get('recipient_address')
        cache.set('recipient', recipient, None)
        cache.set('recipient_address', recipient_address, None)
        print(cache.get('recipient'))
        print(cache.get('recipient_address'))
        return HttpResponseRedirect(reverse('europarts_old_2:add-item-to-quotation', args=(request.POST.get('auto_parts'),)))

    auto_parts = AutoPart.objects.all()

    quotation = cache.get_or_set('quotation', dict(), None)

    context = {
        "auto_parts": auto_parts,
        "quotation": quotation,
        "recipient": cache.get('recipient'),
        "recipient_address": cache.get('recipient_address'),
    }
    return render(request, "europarts/create-quotation.html", context)


def add_item_to_quotation(request, pk):
    quotation = cache.get_or_set('quotation', dict(), None)

    try:
        qty = quotation[pk] # see if key exists
    except KeyError:
        quotation[pk] = 1 # if not then create key with qty = 1
        qty = quotation[pk]
        cache.set('quotation', quotation, None)
    else:
        qty += 1 # if key exists then add 1 to qty
        quotation[pk] = qty
        cache.set('quotation', quotation, None)

    # return JsonResponse(cache.get('quotation'))
    return HttpResponseRedirect(reverse('europarts_old_2:create-quotation'))


def remove_item_from_quotation(request, pk):
    quotation = cache.get_or_set('quotation', dict(), None)

    try:
        qty = quotation[pk] # see if key exists
    except KeyError:
        # return JsonResponse(cache.get('quotation')) # if not then end view by returning JSON
        return HttpResponseRedirect(reverse('europarts_old_2:create-quotation'))
    else:
        if qty > 1: # if key exists then check if qty is more than 1
            qty -= 1
            quotation[pk] = qty
            cache.set('quotation', quotation, None)
        else: # if qty is less than 1 then delete key
            del quotation[pk]
            cache.set('quotation', quotation, None)

    # return JsonResponse(cache.get('quotation'))
    return HttpResponseRedirect(reverse('europarts_old_2:create-quotation'))


def clear_quotation(request):
    quotation = dict()
    cache.set('quotation', quotation, None)
    cache.set('recipient', '', None)
    cache.set('recipient_address', '', None)
    return HttpResponseRedirect(reverse('europarts_old_2:create-quotation'))


def generate_quotation(request):
    quotation = cache.get('quotation')
    recipient = cache.get('recipient')
    recipient_address = cache.get('recipient_address')
    t = datetime.now()
    ref_no = t.strftime('%m%d%Y%H%M%S')

    if bool(quotation):
        q_obj = Quotation.objects.create(ref_no=ref_no, recipient=recipient, recipient_address=recipient_address, total=0)

        for key, value in quotation.items():
            auto_part = AutoPart.objects.get(id=key)
            price = Product.objects.filter(auto_part=auto_part).latest().selling_price

            if price is None:
                q_obj.delete()
                raise Http404

            total = price * value

            qp_obj = QuotationProduct.objects.create(quotation=q_obj, auto_part=auto_part, price=price, quantity=value, total=total)
            q_obj.total += total
            q_obj.save()

        qc_obj = QuotationCode.objects.create(quotation=q_obj, user=request.user, code=str(uuid.uuid4().int)[:6])

    return HttpResponseRedirect(reverse('europarts_old_2:clear-quotation'))


class QuotationListView(generic.ListView):
    model = Quotation
    template_name = "europarts/quotation-listview.html"
    context_object_name = "quotations"


def quotation_details(request, pk):
    q_obj = Quotation.objects.get(id=pk)

    is_euro_admin = request.user.groups.filter(name='EuropartsAdmin').exists()
    try:
        qc_obj = QuotationCode.objects.get(quotation=q_obj, user=request.user, allowed=True)
    except QuotationCode.DoesNotExist:
        has_access_code = False
        work_order_printed = False # so that it doesn't show error when called in context dict
    else:
        has_access_code = True
        work_order_printed = qc_obj.work_order_printed

    # words = num2words(q_obj.total)

    if is_euro_admin or has_access_code:
        qp_obj = QuotationProduct.objects.filter(quotation=q_obj)

        context = {
            "pk": pk,
            "work_order_printed": work_order_printed,
            "products": qp_obj,
            "total": q_obj.total,
            "recipient": q_obj.recipient,
            "recipient_address": q_obj.recipient_address,
            # "words": words,
        }
    else:
        return HttpResponseRedirect(reverse('europarts_old_2:quotation-access-code', args=(pk,)) + '?next=' + reverse('europarts_old_2:quotation-details', args=(pk,)))
    return render(request, "europarts/quotation-details.html", context)


def quotation_access_code(request, pk):
    quotation = Quotation.objects.get(id=pk)

    if request.method == "POST":
        code = request.POST['access_code']

        try:
            qc_obj = QuotationCode.objects.get(quotation=quotation, user=request.user)
        except:
            pass
        else:
            if qc_obj.code == code:
                qc_obj.allowed = True
                qc_obj.save()
            return HttpResponseRedirect(reverse('europarts_old_2:quotation-details', args=(pk,)))

    else:
        try:
            qc_obj = QuotationCode.objects.get(quotation=quotation, user=request.user)
        except QuotationCode.DoesNotExist:
            QuotationCode.objects.create(quotation=quotation, user=request.user, code=str(uuid.uuid4().int)[:6])
        else:
            if qc_obj.allowed:
                return HttpResponseRedirect(request.GET.get('next', '/europarts_old_2/')) # return to original quotation page

    return render(request, "europarts/quotation-access-code.html")


# APIs

def filter_auto_type_with_brand(request, pk):
    brand = Brand.objects.get(id=pk)
    auto_types = AutoType.objects.filter(brand=brand)

    context = {
        "auto_types": auto_types,
    }
    return render(request, "europarts/filter_auto_types_with_brand.html", context)


def fetch_auto_part(request, part_no, brand_pk):
    auto_part = AutoPart.objects.get(part_no=part_no, brand_id=brand_pk)
    response = {"description": auto_part.description}
    return JsonResponse(response)


def fetch_product(request, pk):
    auto_part = AutoPart.objects.get(id=pk)
    product = Product.objects.filter(auto_part=auto_part).latest()
    response = {"description": auto_part.description, "price": product.selling_price}
    return JsonResponse(response)


def disable_work_order_print(request, pk):
    quotation = Quotation.objects.get(id=pk)
    quotation_code = QuotationCode.objects.get(quotation=quotation, user=request.user)
    quotation_code.work_order_printed = True
    quotation_code.save()
    return JsonResponse({"disabled": quotation_code.work_order_printed})

