from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^basket_adding/$', views.basket_adding, name='basket_adding'),

]