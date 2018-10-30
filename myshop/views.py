# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from .models import Category, Product, Brand
from django.utils.text import slugify
from django.shortcuts import redirect
from .util import paginate

# Create your views here.

def ProductList(request, category_slug=None):

    products = Product.objects.filter(available=True)
    context = paginate(products, 4, request, {}, var_name='products')
    return render(request, 'myshop/product/list.html',context )

def ProductListByCategory(request, category_slug ):
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(available=True, category=category)
        brands = Brand.objects.filter(category=category)
        context = paginate(products, 4, request, {}, var_name='products')
    return render(request, 'myshop/product/list_by_category.html', context)


def ProductListByBrand(request, category_slug, brand_slug ):

    if category_slug:
        brands = get_object_or_404(Brand, category__slug=category_slug, slug=brand_slug)
        products = Product.objects.filter(available=True, brand=brands)
        context = paginate(products, 4, request, {}, var_name='products')
    return render(request, 'myshop/product/list_by_brand.html', context)


def ProductDetail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()
    return render(request, 'myshop/product/detail.html', {'product': product})

class CreateProduct(CreateView):
    model = Product
    fields = ('category', 'brand', 'name', 'image', 'description', 'price', 'stock', 'available',    )
    template_name = 'myshop/product/create_product.html'

    def form_valid(self, form):

        model = form.save(commit=False)
        model.slug = slugify(model.name)
        model.save()
        return redirect('myshop:CreateProduct')
