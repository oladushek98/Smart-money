from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(View):
    def get(self, request, **kwargs):

        if request.user.is_authenticated:
            return redirect(self.get_success_url(request))

        return render(request, 'index.html', context={})

    def get_success_url(self, request, **kwargs):
        return reverse_lazy('userpage')


class UserpageView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        return render(request, 'userpage.html', context={})
