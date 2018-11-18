# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Category, Product, Brand, Reply

# Register your models here.
class ReplyInProductInline(admin.TabularInline):
    model = Reply
    fields = ['message', 'author']
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug',]
    prepopulated_fields = {'slug': ('name', )}

class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category']
    prepopulated_fields = {'slug': ('name', )}

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name', )}
    inlines = [ReplyInProductInline]

class ReplyAdmin(admin.ModelAdmin):
    list_display = ['author', 'product', 'message', 'created', 'updated']
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Reply, ReplyAdmin)
