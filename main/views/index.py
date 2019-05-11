import json

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from main.forms import IncomeForm, AccountForm, CostForm, TransactionCreateForm
from main.models import Income, Account, Cost, Transaction
from main.utils import convert_currency


class IndexView(View):
    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url(request))

        return render(request, 'index.html', context={})

    def get_success_url(self, request, **kwargs):
        return reverse_lazy('userpage')


def calculate_cost_amount(cost):
    amount = 0
    for transaction in cost.destination.filter(delete=False).all():
        if cost.currency == transaction.choice_currency:
            amount += transaction.amount
        else:
            amount += convert_currency(transaction.amount,
                                       transaction.choice_currency,
                                       cost.currency)
    return amount


def calculate_income_amount(income):
    amount = 0
    for transaction in income.source.filter(delete=False).all():
        if income.currency == transaction.choice_currency:
            amount += transaction.amount
        else:
            amount += convert_currency(transaction.amount,
                                       transaction.choice_currency,
                                       income.currency)
    return amount


def calculate_account_amount(account):
    amount = 0
    for transaction in account.destination.filter(delete=False).all():
        if account.currency == transaction.choice_currency:
            amount += transaction.amount
        else:
            amount += convert_currency(transaction.amount,
                                       transaction.choice_currency,
                                       account.currency)

    for transaction in account.source.filter(delete=False).all():
        if account.currency == transaction.choice_currency:
            amount -= transaction.amount
        else:
            amount -= convert_currency(transaction.amount,
                                       transaction.choice_currency,
                                       account.currency)

    return amount


class UserpageView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        data_income = [['Element', 'amount', {'role': 'style'}], ]
        data_account = [['Element', 'amount', {'role': 'style'}], ]
        data_cost = [['Element', 'amount', {'role': 'style'}], ]

        incoms = list(Income.objects.filter(delete=False,
                                            user_id=request.user.id).all())
        for incom in incoms:
            incom.amount = calculate_income_amount(incom)
            data_income.append(
                [incom.name.replace('\"', '~'), incom.amount, 'blue'])

        accounts = list(Account.objects.filter(delete=False,
                                               user_id=request.user.id).all())
        for account in accounts:
            account.amount = calculate_account_amount(account)
            data_account.append(
                [account.name.replace('\"', '~'), account.amount, 'gold'])

        costs = list(Cost.objects.filter(delete=False,
                                         user_id=request.user.id).all())
        for cost in costs:
            cost.amount = calculate_cost_amount(cost)
            data_cost.append(
                [cost.name.replace('\"', '~'), cost.amount, 'green'])

        transactions = list(
            Transaction.objects.filter(delete=False,
                                       user_id=request.user.id).all()[:9])
        for transaction in transactions:
            transaction.data_from = transaction.data_from.__str__()

        income_create_from = IncomeForm()
        account_create_form = AccountForm()
        cost_create_form = CostForm()
        add_transaction = TransactionCreateForm()
        if len(data_income) == 1:
            data_income.append(["no incoms", 0, '#000'])
        if len(data_account) == 1:
            data_account.append(["no accounts", 0, '#000'])
        if len(data_cost) == 1:
            data_cost.append(["no costs", 0, '#000'])
        return render(request, 'user/userpage.html',
                      context={'INCOMES': incoms,
                               'ACCOUNTS': accounts,
                               'COSTS': costs,
                               'TRANSACTIONS': transactions,
                               'INCOME_CREATE_FORM': income_create_from,
                               'ADD_TRANSACTION_FORM': add_transaction,
                               'ACCOUNT_CREATE_FORM': account_create_form,
                               'COST_CREATE_FORM': cost_create_form,
                               'data_income': json.dumps(data_income),
                               'data_account': json.dumps(data_account),
                               'data_cost': json.dumps(data_cost),
                               })
