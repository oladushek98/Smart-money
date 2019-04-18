from main.models import Account
from django.urls import reverse_lazy
from django.views.generic import UpdateView


class AccountUpdateView(UpdateView):
    model = Account
    fields = ['id', 'name', 'amount', 'currency', 'take_into_balance']
    template_name = 'account/update_account.html'

    def get_success_url(self):
        return reverse_lazy('userpage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = self.object.id
        return context