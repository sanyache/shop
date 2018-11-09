# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login as auth_login
from .forms import SignUpForm, ProfileForm, UserForm
from .models import StProfile
from django.contrib.auth.models import User
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('myshop:ProductList')
    else:
        form = SignUpForm()
    return render(request, 'myshop/account/signup.html', {'form': form})

def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.stprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

        return HttpResponseRedirect(reverse('myshop:ProductList'))
            #render(request, 'students/my_account.html',{'user_form': user_form, 'profile_form': profile_form})
    else:
        user_id = User.objects.get(pk= request.user.pk)
        user_form = UserForm(instance= request.user)
        user_id.stprofile, created = StProfile.objects.get_or_create(user=user_id)
        profile_form = ProfileForm(instance= request.user.stprofile)
    return render(request, 'myshop/account/my_account.html',{'user_form': user_form, 'profile_form': profile_form} )