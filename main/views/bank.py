import csv
import os

from django.contrib.auth.models import User
from django.db.models import Q
from django.forms.utils import ErrorList
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from main.forms import UploadFile
from main.models import UserAdditionalInfo, Account, Income, Cost, Transaction
from main.tasks import bank_integration
from main.utils import convert_currency


class BankIntegrationView(LoginRequiredMixin, View):

    def get(self, request):
        file_form = UploadFile()
        if 'error' in request.GET:
            error = ErrorList()
            error.data.append(request.GET['error'])
            file_form.errors['file'] = error
        return render(request, 'bank/bank_integration.html',
                      context={'file_form': file_form})

    def post(self, request):
        user = UserAdditionalInfo.objects.filter(
            user_id=request.user.id).first()

        login = user.bank_login
        password = user.bank_password

        bank_integration.delay(login, password, request.user.id)

        return redirect('userpage')


class UploadCSVView(View):
    def handle_file(self, file, user):
        with open(f'main\\static\\data\\csv{user.id}.csv',
                  'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        cost, income, account = None, None, None
        with open(f'main\\static\\data\\csv{user.id}.csv',
                  'r') as file:
            reader = csv.reader(file)
            row_num = 0
            for row in reader:
                if row_num == 0:
                    account_name = row[0].split(':')[1].split('-')[0]
                    amount = int(float(row[-7].split(':')[-1].split(' ')[0]))
                    acc_cur = row[-7].split(':')[-1].split(' ')[1]
                    account = Account.objects.filter(
                        Q(user=user) &
                        Q(name__startswith=account_name) &
                        Q(delete=False)).first()
                    if not account:
                        account = Account(name=account_name,
                                          user=user,
                                          amount=amount,
                                          currency=acc_cur,
                                          )
                        account.save()

                    income = Income.objects.filter(
                        Q(user=user) &
                        Q(name__startswith=account_name) &
                        Q(delete=False)
                    ).first()
                    if not income:
                        income = Income(name=account_name,
                                        user=user,
                                        currency=acc_cur)
                        income.save()

                    cost = Cost.objects.filter(
                        Q(user=user) &
                        Q(name__startswith=account_name) &
                        Q(delete=False)
                    ).first()
                    if not cost:
                        cost = Cost(name=account_name,
                                    user=user,
                                    currency=acc_cur)
                        cost.save()
                elif row_num > 2:
                    for j in range(len(row) - 1, 0, -1):
                        if row[j] == '':
                            continue
                        else:
                            date = row[0].split('.')
                            date.reverse()
                            date = '-'.join(date)
                            amount = int(float(row[j - 3]))
                            cur = row[j - 2]
                            comment = row[1].split()
                            comment = ' '.join(comment)
                            if amount > 0:
                                Transaction(
                                    data_from=date,
                                    user=user,
                                    transaction_from=income,
                                    transaction_to=account,
                                    choice_currency=cur,
                                    amount=amount,
                                    comment=comment[:100]
                                ).save()
                            else:
                                Transaction(
                                    data_from=date,
                                    user=user,
                                    transaction_from=account,
                                    transaction_to=cost,
                                    choice_currency=cur,
                                    amount=-1 * amount,
                                    comment=comment[:100]
                                ).save()
                            break
                row_num += 1
        os.remove(f'main\\static\\data\\csv{user.id}.csv')

    def post(self, request):
        form = UploadFile(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if file.name.split('.')[-1] == 'csv':
                self.handle_file(file, request.user)
                return HttpResponseRedirect('/')

        return HttpResponseRedirect('user/bank?error=неверный формат файла')
