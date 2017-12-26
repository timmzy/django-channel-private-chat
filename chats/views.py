# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.

def logins(request):
    status = 0
    if request.user.is_authenticated:
        return home(request)
    if request.method == "POST":
        if "sign" in request.POST:
            username = request.POST['username']; password = request.POST['password']
            if User.objects.filter(username=username).exists():
                status = 1
                return render(request, 'login.html', locals())
            elif username != "" and password != "":
                user = User.objects.create_user(username=username, password=password)
                user.save()
                user = authenticate(request, username=username, password=password)
                login(request, user)
                return home(request)
        if "log" in request.POST:
            username = request.POST['username']; password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is None:
                status = 2
                return render(request, 'login.html', locals())
            else:
                login(request, user)
                return home(request)
    return render(request, 'login.html', locals())



def home(request):

    return render(request, 'index.html', locals())

def chat(request, username):

    return render(request, 'chat.html', locals())

def logout_view(request):
    logout(request)
    return redirect('logs')