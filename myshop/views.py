# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.generic import CreateView, UpdateView
from .models import Category, Product, Brand, Reply
from django.utils.text import slugify
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from .util import paginate
from .forms import ReplyForm
import json

# Create your views here.

def ProductList(request, category_slug=None):

    products = Product.objects.filter(available=True)
    context = paginate(products, 4, request, {}, var_name='products')
    return render(request, 'myshop/product/list.html',context )

def ProductStock(request):
    products = Product.objects.all()
    return render(request, 'myshop/product/stock.html', locals())

def ProductListByCategory(request, category_slug ):
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(available=True, category=category)
        brands = Brand.objects.filter(category=category)
        context = paginate(products, 4, request, {}, var_name='products')
    return render(request, 'myshop/product/list_by_category.html', context)

def StockListByCategory(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    context = {'products': products}
    data = dict()
    data['html_form'] = render_to_string('myshop/product/includes/partial_stock_list.html', context, request)
    return JsonResponse(data)


def ProductListByBrand(request, category_slug, brand_slug ):

    if category_slug:
        brands = get_object_or_404(Brand, category__slug=category_slug, slug=brand_slug)
        products = Product.objects.filter(available=True, brand=brands)
        context = paginate(products, 4, request, {}, var_name='products')
    return render(request, 'myshop/product/list_by_brand.html', context)

def StockListByBrand(request, category_slug, brand_slug):
    brands = get_object_or_404(Brand, category__slug=category_slug, slug=brand_slug)
    products = Product.objects.filter(available=True, brand=brands)
    context = {'products': products}
    data = dict()
    data['html_form'] = render_to_string('myshop/product/includes/partial_stock_list.html', context, request)
    return JsonResponse(data)


def ProductDetail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()
    replies = Reply.objects.filter(product=product)
    return render(request, 'myshop/product/detail.html', {'product': product, 'replies': replies})

class CreateProduct(CreateView):
    model = Product
    fields = ('category', 'brand', 'name', 'image', 'description', 'price', 'stock', 'available',)
    template_name = 'myshop/product/create_product.html'

    def form_valid(self, form):

        model = form.save(commit=False)
        model.slug = slugify(model.name)
        model.save()
        return redirect('myshop:CreateProduct')

class ProductEdit(UpdateView):
    model = Product
    fields = fields = ['name', 'category', 'brand', 'description', 'price', 'stock', 'image']
    template_name = 'myshop/product/product_edit.html'

    def get_success_url(self):
        return reverse('myshop:Stock')

def ProductDelete(request, pk, slug):
    product = get_object_or_404(Product, pk=pk, slug=slug)
    data = dict()
    if request.method == 'POST':
        product.delete()
        data['form_is_valid'] = True
        products = Product.objects.all()
        data['html_order_list'] = render_to_string('myshop/product/includes/partial_stock_list.html', {'products': products})
    else:
        context = {'product': product}
        data['html_form'] = render_to_string('myshop/product/product_delete.html', context, request)
    return JsonResponse(data)


def product_search_tph(request):
    q = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=q)
    data = []
    for product in products:
        new = {'q': product.name}
        if not new in data:
            data.append(new)
    return HttpResponse(json.dumps(data), content_type="application/json")

def product_search(request):
    data = dict()
    if request.method == 'POST':
        search = request.POST.get('search_product')
        products = Product.objects.filter(name__iexact=search)
        data['form_is_valid'] = True
        data['html_order_list'] = render_to_string('myshop/product/includes/partial_stock_list.html', {'products': products})

    return JsonResponse(data)

def reply_product(request, pk, slug, id):
    product = get_object_or_404(Product, pk=pk, slug=slug)
    data = dict()
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply, created = Reply.objects.get_or_create(product=product, message=form.cleaned_data.get('message'), author=request.user)
            if int(id) > 0:
                reply.parent = int(id)
                reply.save()
            replies = Reply.objects.filter(product=product)
            data['form_is_valid'] = True

            data['html_order_list'] = render_to_string('myshop/product/includes/partial_replay_list.html', {'replies': replies, 'product': product})
    else:
        form = ReplyForm
        context = {'form': form, 'product': product}
        data['html_form'] = render_to_string('myshop/product/reply_add.html', context, request)
    return JsonResponse(data)
