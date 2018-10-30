# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Status, Order, ProductInOrder, ProductInBasket

# Register your models here.

class ProductInOrderInline(admin.TabularInline):

    model = ProductInOrder
    fields = ['product', 'nmb', 'price_per_item', 'total_price', 'is_active']
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
    list_display = ['order', 'product', 'nmb',  'get_stock', 'price_per_item', 'total_price', 'is_active']
    
    
    class Meta:
        model = ProductInOrder
    def get_stock(self, obj):
        return obj.product.stock


class ProductInBasketAdmin (admin.ModelAdmin):
    list_display = [field.name for field in ProductInBasket._meta.fields]

    class Meta:
        model = ProductInBasket

admin.site.register(Status, StatusAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductInOrder, ProductInOrderAdmin)
admin.site.register(ProductInBasket, ProductInBasketAdmin)
