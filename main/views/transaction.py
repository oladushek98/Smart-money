from django.shortcuts import render

from main.forms import TransactionUpdateForm
from main.models import Transaction
from django.urls import reverse_lazy
from django.views.generic import FormView


class TransactionUpdateView(FormView):
    form_class = Transaction
    template_name = 'transaction/update_transaction.html'

    def get(self, request, *args, **kwargs):
        transaction_id = int(request.path.split('/')[-1])
        transaction = Transaction.objects.filter(id=transaction_id).first()

        form = TransactionUpdateForm(**transaction)

        form.id = transaction.id
        return render(request, template_name=self.template_name,
                      context={'form': form})

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
