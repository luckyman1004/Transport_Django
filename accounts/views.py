from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
import re
from django.http import HttpResponseRedirect

# Create your views here.


def account(request):
    return render(request, 'accounts/loginform.html')


def login(request):
    user_name = request.POST['loginemail']
    password = request.POST['loginPassword']
    values = {
        'user_name': user_name,
    }
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex, user_name):
        user = auth.authenticate(email=user_name, password=password)
    else:
        user = auth.authenticate(username=user_name, password=password)
    if user is not None:
        auth.login(request, user)
        return redirect('/')
    else:
        message = {
            'from': 'login',
            'error': 'Invalid Credentials',
            'value': values
        }
        return render(request, 'accounts/loginform.html', message)
    # return render(request, './accounts/login.html', {'data': 'login is successful'})


def register(request):
    user_name = request.POST['username']
    full_name = str(request.POST['full_name'])
    email = request.POST['emailAddress']
    password = request.POST['password']
    values = {
        'user_name': user_name,
        'full_name': full_name,
        'email': email,
    }
    first_name, last_name = full_name.rsplit(maxsplit=1)
    if User.objects.filter(username=user_name).exists():
        message = {
            'from': 'signup',
            'error': 'User name is already taken',
            'values': values
        }
        return render(request, 'accounts/loginform.html', message)
    else:
        user = User.objects.create_user(username=user_name, password=password, email=email, first_name=first_name, last_name=last_name)
        user.save()
        return redirect('/')
    # return render(request, 'accounts/login.html', {'data': 'registration is successful'})


def logout(request):
    auth.logout(request)
    return redirect('/')
