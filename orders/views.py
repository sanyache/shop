# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from .models import ProductInBasket, ProductInOrder, Order
from myshop.models import Product
from .forms import CheckContactForm, OrderForm, ProductInOrderForm
from django.contrib.auth.models import User
import json

# Create your views here.

def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key

    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")
    is_delete = data.get("is_delete")

    if is_delete == 'true':
        ProductInBasket.objects.filter(id=product_id).update(is_active=False)
    else:
        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id,
                                                                     is_active=True, defaults={"nmb": nmb})
        if not created:

            new_product.nmb += int(nmb)
            new_product.save(force_update=True)

    #common code for 2 cases
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    products_total_nmb = products_in_basket.count()
    return_dict["products_total_nmb"] = products_total_nmb

    return_dict["products"] = list()

    for item in  products_in_basket:
        product_dict = dict()
        product_dict["id"] = item.id
        product_dict["name"] = item.product.name
        product_dict["price_per_item"] = item.price_per_item
        product_dict["nmb"] = item.nmb
        return_dict["products"].append(product_dict)

    return JsonResponse(return_dict)

def checkout(request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    form = CheckContactForm(request.POST or None)
    if request.POST :

        if form.is_valid():
            data = request.POST
            name = data.get('name', '123')
            phone = data['phone']
            user, created = User.objects.get_or_create(username=phone, defaults={'first_name': name})

            order = Order.objects.create(user=user, customer_name=name, customer_phone=phone, status_id=1)
            for key, value in data.items():
                if key.startswith('product_in_basket.nmb_'):
                    product_in_basket_id = key.split('product_in_basket.nmb_')[1]
                    product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)
                    product_in_basket.nmb = value
                    product_in_basket.order = order
                    product_in_basket.save(force_update=True)

                    ProductInOrder.objects.create(product=product_in_basket.product, nmb=product_in_basket.nmb,
                                                  price_per_item=product_in_basket.price_per_item,
                                                  total_price=product_in_basket.total_price, order=order)
    return render(request, 'myshop/checkout.html', locals())

def order_list(request):
    orders = Order.objects.all().order_by('-updated')
    return render(request, 'myshop/order/order_list.html', {'orders': orders})

def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    products_in_order = ProductInOrder.objects.filter(order__pk=order.id)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()
            order.save()
            data = request.POST
            for key, value in data.items():

                if key.startswith('product_in_order.nmb_'):
                    product_in_order_id = key.split('product_in_order.nmb_')[1]
                    product_in_order = ProductInOrder.objects.get(id=product_in_order_id)
                    product_in_order.nmb = value
                    product_in_order.order = order
                    is_activ = 'is-active_'+product_in_order_id
                    if is_activ in data.keys():
                        product_in_order.is_active = True
                    else:
                        product_in_order.is_active = False
                    product_in_order.order = order
                    product_in_order.save(force_update=True)
                    # Stock
                    product_id = product_in_order.product.id
                    product = Product.objects.get(id=product_id)
                    product.stock -= int(value)
                    product.save(force_update=True)
            return redirect('orders:order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'myshop/order/order_edit.html', locals())

def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    data = dict()
    if request.method == 'POST':
        order.delete()
        data['form_is_valid'] = True
        orders = Order.objects.all().order_by('-updated')
        data['html_order_list'] = render_to_string('myshop/order/includes/partial_order_list.html', {'orders': orders})
    else:
        context = {'order': order}
        data['html_form'] = render_to_string('myshop/order/includes/partial_order_delete.html', context, request)
    return JsonResponse(data)

def product_add(request, pk):
    data = dict()
    order = get_object_or_404(Order, pk=pk)
    id = order.id
    if request.method == 'POST':
        form = ProductInOrderForm(request.POST)
        product_id = request.POST.get('product')
        product = Product.objects.get(pk=product_id)
        if form.is_valid():
            product_in_order = form.save(commit=False)
            product_in_order.price_per_item = product.price
            product_in_order.order = order
            product_in_order.save()
            products_in_order = ProductInOrder.objects.filter(order__pk=order.id)
            data['form_is_valid'] = True
            data['html_order_list'] = render_to_string('myshop/order/includes/partial_order_product_list.html', {'products_in_order': products_in_order})
    else:
        form = ProductInOrderForm()
        context = {'form': form, 'id':id}
        data['html_form'] = render_to_string('myshop/order/includes/partial_order_product_add.html', context, request)
    return JsonResponse(data)

def order_search_tph(request):
    q = request.GET.get('q', '')
    orders = Order.objects.filter(customer_phone__icontains=q)
    data = []
    for order in orders:
        new = {'q': order.customer_phone}
        if not new in data:
            data.append(new)
    return HttpResponse(json.dumps(data), content_type="application/json")

def order_search(request):
    data = dict()
    if request.method == 'POST':
        search = request.POST.get('search_order')
        orders = Order.objects.filter(customer_phone__iexact=search)
        data['form_is_valid'] = True
        data['html_order_list'] = render_to_string('myshop/order/includes/partial_order_list.html', {'orders': orders})

    return JsonResponse(data)