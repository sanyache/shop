from django.conf.urls import url
from . import views
from .views import CreateProduct, ProductEdit

urlpatterns = [
    url(r'^$', views.ProductList, name='ProductList'),
    url(r'^stock/$', views.ProductStock, name='Stock'),
    url(r'^stock/search_tph/$', views.product_search_tph, name='search_tph'),
    url(r'^stock/searh/$', views.product_search, name='search'),
    url(r'^product/$', CreateProduct.as_view(), name='CreateProduct'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.ProductListByCategory, name='ProductListByCategory'),
    url(r'^stock/(?P<category_slug>[-\w]+)/$', views.StockListByCategory, name='StockListByCategory'),
    url(r'^(?P<category_slug>[-\w]+)/brand/(?P<brand_slug>[-\w]+)/$', views.ProductListByBrand, name='ProductListByBrand'),
    url(r'^stock/(?P<category_slug>[-\w]+)/brand/(?P<brand_slug>[-\w]+)/$', views.StockListByBrand, name='StockListByBrand'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.ProductDetail, name='ProductDetail'),
    url(r'^product_edit/(?P<id>\d+)/(?P<slug>[-\w]+)/$', ProductEdit.as_view(), name='ProductEdit'),
    url(r'^product_delete/(?P<pk>\d+)/(?P<slug>[-\w]+)/$', views.ProductDelete, name='ProductDelete')
]