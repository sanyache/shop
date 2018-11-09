# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from myshop.models import Product
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=24, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return "Статус %s" % (self.name)

    class Meta:
        verbose_name = 'Статус замовлення'
        verbose_name_plural = 'Статуси замовлення'

class Order(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, default=None, verbose_name='Користувач')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Загальна вартість')
    customer_name = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name="Ім'я")
    customer_email = models.EmailField(blank=True, null=True, default=None, verbose_name='Email')
    customer_phone = models.CharField(max_length=48, blank=True, null=True, default=None, verbose_name='Телефон')
    customer_address = models.CharField(max_length=128, blank=True, null=True, default=None, verbose_name='Адреса')
    comments = models.TextField(blank=True, null=True, default=None, verbose_name='Коментар')
    status = models.ForeignKey(Status, verbose_name='Статус')
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Створено')
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name='Оновлено')

    def __unicode__(self):
        return "Замовлення %s%s" %(self.id, self.status.name)

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'

    def save(self, *args, **kwargs):

        super(Order, self).save(*args, **kwargs)

class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, default=None)
    product = models.ForeignKey(Product, blank=True, null=True, default=None, verbose_name='Назва')
    nmb = models.IntegerField(default=1, verbose_name='Кількість')
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)#price*nmb
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = 'Товар в заказі'
        verbose_name_plural = 'Товари в заказі'


    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        self.price_per_item = price_per_item
        self.total_price = int(self.nmb) * price_per_item

        super(ProductInOrder, self).save(*args, **kwargs)



def product_in_order_post_save(sender, instance, created, **kwargs):
    order = instance.order
    all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)

    order_total_price = 0
    for item in all_products_in_order:
        order_total_price += item.total_price

    instance.order.total_price = order_total_price
    instance.order.save(force_update=True)


post_save.connect(product_in_order_post_save, sender=ProductInOrder)

class ProductInBasket(models.Model):
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None)
    order = models.ForeignKey(Order, blank=True, null=True, default=None)
    product = models.ForeignKey(Product, blank=True, null=True, default=None)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)#price*nmb
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = 'Товар в корзині'
        verbose_name_plural = 'Товари в корзині'


    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        self.price_per_item = price_per_item
        self.total_price = int(self.nmb) * price_per_item

        super(ProductInBasket, self).save(*args, **kwargs)


