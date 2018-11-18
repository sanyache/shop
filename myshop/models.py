# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import Truncator
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def get_absolute_url(self):
        return reverse('myshop: ProductListByCategory', args=[self.slug])

    def __unicode__(self):
        return u"%s"%(self.name)

class Brand(models.Model):
    name = models.CharField(max_length=200, db_index=True, blank=True, null=True, default=None)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, blank=True, null=True, default=None)
    category = models.ForeignKey(Category, related_name='brands', verbose_name='Категорія')
    class Meta:
        ordering = ['name']
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренди'


    def __unicode__(self):
        return u"%s"%(self.name)


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', verbose_name='Категорія', blank=True, null=True, default=None)
    brand = models.ForeignKey(Brand, related_name='products', verbose_name='Бренд', blank=True, null=True, default=None)
    name = models.CharField(max_length=200, db_index=True, verbose_name='Назва')
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, verbose_name='Зображення товару')
    description = models.TextField(blank=True, verbose_name='Опис товару')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна')
    stock = models.PositiveIntegerField(verbose_name='На складі')
    available = models.BooleanField(default=True, verbose_name='Доступний')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        index_together = [['id', 'slug']]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'

    def get_absolute_url(self):
        return reverse('myshop:ProductDetail', args=[self.id, self.slug])

    def __unicode__(self):
        return u"%s"%(self.name)

class Reply(models.Model):
    message = models.TextField(max_length=4000, verbose_name='коментар')
    product = models.ForeignKey(Product, related_name='replies')
    author = models.ForeignKey(User, related_name='replies')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    parent = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'

    def __unicode__(self):
        reply = Truncator(self.message).chars(30)
        return u"%s"%(reply)