from django.shortcuts import render

from main.forms import AccountForm
from main.models import Account
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

        return render(request, template_name=self.template_name, context={'form': form})

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        amount = form.cleaned_data.get('amount')
        currency = form.cleaned_data.get('currency')
        Account.objects.filter(id=int(self.request.path.split('/')[-1])).update(
            name=name, amount=amount, currency=currency)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('userpage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = self.object.id
        return context