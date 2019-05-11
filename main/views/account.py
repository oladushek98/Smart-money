import json

from django.db.models import Q, Sum
from django.shortcuts import render

from main.forms import AccountForm
from main.models import Account, Transaction
from django.urls import reverse_lazy
from django.views.generic import UpdateView, FormView


class AccountUpdateView(FormView):
    form_class = AccountForm
    template_name = 'account/update_account.html'

    def get_history_chart_data(self, account):
        account_create_date = account.create_on
        account_history_data = [['дата', 'состояние счета'],
                                [account_create_date.__str__(), account.amount]]

        dates_query = Transaction.objects.filter(Q(user=self.request.user.id) &
                                                 Q(delete=False) & (
                Q(transaction_from=account.id) | Q(transaction_to=account.id))).values(
            'data_from').order_by('data_from').distinct()
        dates = list(map(lambda x: x['data_from'].__str__(), dates_query))

        amount = account.amount
        for date in dates:
            calculate = Transaction.objects.filter(
                Q(delete=False) & Q(user=self.request.user.id) & Q(
                    data_from=date)).aggregate(
                plus=Sum('amount', filter=(Q(transaction_to=account.id))),
                minus=Sum('amount', filter=(Q(transaction_from=account.id))))
            amount += calculate['plus'] if calculate['plus'] is not None else 0
            amount -= calculate['minus'] if calculate[
                                                'minus'] is not None else 0

            account_history_data.append([date, amount])

        return account_history_data

    def get_history_to_chart_data(self, account):
        dest_query = list(Transaction.objects.filter(
            Q(transaction_to=account.id) & Q(delete=False) & Q(
                user=self.request.user.id))
                          .order_by('transaction_from__id')
                          .values('transaction_from__name')
                          .annotate(Sum('amount')))
        return [list(income.values()) for income in dest_query]

    def get_history_from_chart_data(self, account):
        source_query = list(Transaction.objects.filter(
            Q(transaction_from=account.id) & Q(delete=False) & Q(
                user=self.request.user.id))
                            .order_by('transaction_to__id')
                            .values('transaction_to__name')
                            .annotate(Sum('amount')))
        return [list(cost.values()) for cost in source_query]

    def get(self, request, *args, **kwargs):
        account_id = int(request.path.split('/')[-1])
        account = Account.objects.filter(id=account_id).first()

        name = account.name
        amount = account.amount
        currency = account.currency
        take_into_balance = account.take_into_balance

        form = AccountForm(initial={'name': name,
                                    'amount': amount,
                                    'currency': currency,
                                    'take_into_balance': take_into_balance})
        form.id = account_id
        form.title = account.name

        account_history_data = self.get_history_chart_data(account)

        destination_history = self.get_history_to_chart_data(account)

        source_history = self.get_history_from_chart_data(account)

        return render(request, template_name=self.template_name,
                      context={'form': form,
                               'data': json.dumps(account_history_data),
                               'data_to': json.dumps(destination_history),
                               'data_from': json.dumps(source_history)})

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        amount = form.cleaned_data.get('amount')
        currency = form.cleaned_data.get('currency')
        boolean = form.data['take_into_balance'] == 'on'
        Account.objects.filter(id=int(self.request.path.split('/')[-1])).update(
            name=name, amount=amount, currency=currency,
            take_into_balance=boolean)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('userpage')
