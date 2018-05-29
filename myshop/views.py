# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Brand

# Create your views here.

def ProductList(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    return render(request, 'myshop/product/list.html', locals())

def ProductListByCategory(request, category_slug ):
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(available=True, category=category)
        brands = Brand.objects.filter(category=category)
    return render(request, 'myshop/product/list_by_category.html', locals())


def ProductListByBrand(request, category_slug, brand_slug ):

    if category_slug:
        brands = get_object_or_404(Brand, category__slug=category_slug, slug=brand_slug)
        products = Product.objects.filter(available=True, brand=brands)
    return render(request, 'myshop/product/list_by_brand.html', locals())


def ProductDetail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()
    return render(request, 'myshop/product/detail.html', {'product': product})