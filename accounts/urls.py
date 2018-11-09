from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views as accounts_views


urlpatterns = [
    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='myshop/account/login.html'), name='login'),
    url(r'^account/$', accounts_views.update_profile, name='my_account'),

]