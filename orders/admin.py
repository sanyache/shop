# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Status, Order, ProductInOrder, ProductInBasket

# Register your models here.

class ProductInOrderInline(admin.TabularInline):
    model = ProductInOrder
    extra = 0

class StatusAdmin (admin.ModelAdmin):
    list_display = [field.name for field in Status._meta.fields]

    class Meta:
        model = Status

class OrderAdmin (admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]
    inlines = [ProductInOrderInline]

    class Meta:
        model = Order

class ProductInOrderAdmin (admin.ModelAdmin):
    list_display = [field.name for field in ProductInOrder._meta.fields]

    class Meta:
        model = ProductInOrder

class ProductInBasketAdmin (admin.ModelAdmin):
    list_display = [field.name for field in ProductInBasket._meta.fields]

    class Meta:
        model = ProductInBasket

admin.site.register(Status, StatusAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductInOrder, ProductInOrderAdmin)
admin.site.register(ProductInBasket, ProductInBasketAdmin)
