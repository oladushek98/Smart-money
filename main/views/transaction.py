from django.db.models import Q, Sum
from django.shortcuts import render

from main.forms import TransactionUpdateForm
from main.models import Transaction, Account
from django.urls import reverse_lazy
from django.views.generic import FormView


class TransactionUpdateView(FormView):
    form_class = Transaction
    template_name = 'transaction/update_transaction.html'

    def get(self, request, *args, **kwargs):
        transaction_id = int(request.path.split('/')[-1])
        transaction = Transaction.objects.filter(id=transaction_id).first()

        form = TransactionUpdateForm(initial=transaction.dict)

        form.id = transaction.id

        source_id = transaction.transaction_to.id

        obj = Account.objects.filter(id=source_id).first()
        amount = 0 if obj is None else obj.amount

        calculate = Transaction.objects.filter(
            (Q(transaction_from=source_id) | Q(transaction_to=source_id)) & Q(
                id__lt=transaction.id)).aggregate(
            plus=Sum('amount', filter=(Q(transaction_to=source_id))),
            minus=Sum('amount', filter=(Q(transaction_from=source_id))))

        amount += calculate['plus'] if calculate['plus'] is not None else 0
        amount -= calculate['minus'] if calculate['minus'] is not None else 0

        data = {
            "labels": ['было на счете', 'транзакция'],
            'datasets': [{
                'data': [amount, transaction.amount],
                'backgroundColor': [
                    'rgba(240, 158, 7, 1)',
                    'rgba(255, 255, 0, 1)',
                ]
            }],
        }

        return render(request, template_name=self.template_name,
                      context={'form': form, 'data': data})

    def form_valid(self, form):
        # name = form.cleaned_data.get('name')
        # monthly_plan = form.cleaned_data.get('monthly_plan')
        # currency = form.cleaned_data.get('currency')
        # Transaction.objects.filter(
        #     id=int(self.request.path.split('/')[-1])).update(name=name,
        #                                                      monthly_plan=monthly_plan,
        #                                                      currency=currency)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('userpage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = self.object.id
        return context
