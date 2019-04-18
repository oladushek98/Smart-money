from main.models import Cost
from django.urls import reverse_lazy
from django.views.generic import UpdateView


class CostUpdateView(UpdateView):
    model = Cost
    fields = ['id', 'name', 'monthly_plan', 'currency']
    template_name = 'cost/update_cost.html'

    def get_success_url(self):
        return reverse_lazy('userpage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = self.object.id
        return context