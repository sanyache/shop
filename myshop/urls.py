from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ProductList, name='ProductList'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.ProductListByCategory, name='ProductListByCategory'),
    url(r'^(?P<category_slug>[-\w]+)/brand/(?P<brand_slug>[-\w]+)/$', views.ProductListByBrand, name='ProductListByBrand'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.ProductDetail, name='ProductDetail'),
]