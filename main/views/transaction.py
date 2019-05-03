import json

from django.db.models import Q, Sum
from django.shortcuts import render

from main.forms import TransactionUpdateForm
from main.models import Transaction, Account
from django.urls import reverse_lazy
from django.views.generic import FormView


class TransactionUpdateView(FormView):
    form_class = TransactionUpdateForm
    template_name = 'transaction/update_transaction.html'

    def get_chart_data(self, transaction):
        destination = Account.objects.filter(id=transaction.transaction_to) \
            .first()

        amount = 0 if destination is None else destination.amount
        amount += Transaction.objects \
            .filter(id__lt=transaction.id,
                    delete=False,
                    user=self.request.user) \
            .aggregate(
            value=Sum('amount', filter=(Q(transaction_to=destination.id))) \
                  - Sum('amount', filter=(Q(transaction_from=destination.id))))

        return [['транзакция', transaction.amount],
                [destination.name.replace('"', '\''), amount['value']]]

    def get(self, request, *args, **kwargs):
        transaction_id = int(request.path.split('/')[-1])
        transaction = Transaction.objects.filter(id=transaction_id).first()

        form = TransactionUpdateForm(initial=transaction.dict)
        form.id = transaction.id

        chart_data = self.get_chart_data(transaction)

        return render(request, template_name=self.template_name,
                      context={'form': form, 'data': json.dumps(chart_data)})

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        Transaction.objects.filter(
            id=int(self.request.path.split('/')[-1])).update(amount=amount)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('userpage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = self.object.id
        return context
