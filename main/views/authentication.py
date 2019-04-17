from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import views
from django.urls import reverse_lazy

import re

from main.models import UserAdditionalInfo


class RegisterView(views.View):
    def get(self, request):
        form = UserCreationForm()
        args = {'form': form}

        return render(request, 'register.html', args)

    def post(self, request):
        form = UserCreationForm(request.POST)
        args = {}
        if form.is_valid():
            form.save()
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = auth.authenticate(
                request,
                username=username,
                password=password
            )

            UserAdditionalInfo.objects.update_or_create(user_id=User.objects.filter(username=username).first().id)

            return redirect('/')

        else:
            exp = r'[a-zA-Z0-9 \&#\;]*\.'
            error = re.findall(exp, str(form.errors))[0]
            error = error.replace('&#39;', '\'')
            args['error'] = error
            form = UserCreationForm()
            args['form'] = form

            return render(request, 'register.html', args)


class LoginView(views.View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, 'login.html')

    def post(self, request):
        args = {}

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            auth.login(request, user)
            args = {'username': username}
            print(user)
            if username == 'admin':
                print(1)
                return redirect('/admin/')
            else:
                print(2)
                return redirect(self.get_success_url(request))

        else:
            args['login_error'] = 'User not found'

        return render(request, 'login.html', args)

    def get_success_url(self, request, **kwargs):
        return reverse_lazy('userpage')


class LogoutView(views.View):
    def get(self, request):
        auth.logout(request)
        return redirect('/')
