import json

from django.db.models import Q, Sum
from django.shortcuts import render

from main.forms import AccountForm
from main.models import Account, Transaction
from django.urls import reverse_lazy
from django.views.generic import UpdateView, FormView


# class AccountUpdateView(UpdateView):
#     model = Account
#     fields = ['id', 'name', 'amount', 'currency', 'take_into_balance']
#     template_name = 'account/update_account.html'
#
#     def get_success_url(self):
#         return reverse_lazy('userpage')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['id'] = self.object.id
#         return context


class AccountUpdateView(FormView):

    form_class = AccountForm
    template_name = 'account/update_account.html'

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

        data = {
            "labels": [account.create_on.__str__()],
            'datasets': [{
                'label': 'на счете',
                'lebels': ['test', 'test2'],
                'fill': 'false',
                "data": [amount],
                'backgroundColor': 'rgba(240, 158, 7, 1)',
                'borderColor': 'rgba(240, 158, 7, 1)',
            }],
        }

        l = list(Transaction.objects.filter(
            Q(transaction_to=account_id) | Q(transaction_from=account_id)).all())
        let = set()
        for i in l:
            let.add(i.data_from.__str__())

        ll = list(let)
        ll.sort()

        for l in ll:
            calculate = Transaction.objects.filter(
                (Q(transaction_from=account_id) | Q(transaction_to=account_id)) & Q(
                    data_from=l)).aggregate(
                plus=Sum('amount', filter=(Q(transaction_to=account_id))),
                minus=Sum('amount', filter=(Q(transaction_from=account_id))))
            amount += calculate['plus'] if calculate['plus'] is not None else 0
            amount -= calculate['minus'] if calculate['minus'] is not None else 0
            data['datasets'][0]['data'].append(amount)
            data['labels'].append(l)

        return render(request, template_name=self.template_name,
                      context={'form': form, 'data': json.dumps(data)})

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
