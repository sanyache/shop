from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^basket_adding/$', views.basket_adding, name='basket_adding'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^orders/$', views.order_list, name='order_list'),
    url(r'^orders/search/$', views.order_search, name='order_search'),
    url(r'^orders/search_tph/$', views.order_search_tph, name='order_search_tph'),
    url(r'^orders/(?P<pk>\d+)/product_add/$', views.product_add, name='product_add'),
    url(r'^orders/(?P<pk>\d+)/edit/$', views.order_edit, name='order_edit'),
    url(r'^orders/(?P<pk>\d+)/delete/$', views.order_delete, name='order_delete'),


]