from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from main.models import UserAdditionalInfo
from main.tasks import bank_integration


class BankIntegrationView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'bank/bank_integration.html')

    def post(self, request):
        user = UserAdditionalInfo.objects.filter(user_id=request.user.id).first()

        login = user.bank_login
        password = user.bank_password

        bank_integration.delay(login, password, request.user.id)

        return render(request, 'user/userpage.html')
