from main.models import Income
from django.urls import reverse_lazy
from django.views.generic import UpdateView


class IncomeUpdateView(UpdateView):
    model = Income
    fields = ['id', 'name', 'monthly_plan', 'currency']
    template_name = 'income/update_income.html'

    def get_success_url(self):
        return reverse_lazy('userpage', args=[self.object.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = self.object.id
        return context