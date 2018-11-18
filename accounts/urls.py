from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views as accounts_views


urlpatterns = [
    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='myshop/account/login.html'), name='login'),
    url(r'^account/$', accounts_views.update_profile, name='my_account'),

    url(r'^reset/$', auth_views.PasswordResetView.as_view(template_name='myshop/account/password_reset.html',success_url='/accounts/reset/done/', email_template_name='myshop/account/password_reset_email.html', subject_template_name='myshop/account/password_reset_subject.txt'), name='password_reset'),
    url(r'^reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='myshop/account/password_reset_done.html'), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',	auth_views.PasswordResetConfirmView.as_view(template_name='myshop/account/password_reset_confirm.html', success_url='/accounts/reset/complete/'), name='password_reset_confirm'),
    url(r'^reset/complete/$', auth_views.PasswordResetCompleteView.as_view(template_name='myshop/account/password_reset_complete.html'),name='password_reset_complete'),

]