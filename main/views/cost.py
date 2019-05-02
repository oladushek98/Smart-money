from django.shortcuts import render

from main.forms import CostForm
from main.models import Cost
from django.urls import reverse_lazy
from django.views.generic import UpdateView, FormView


# class CostUpdateView(UpdateView):
#     model = Cost
#     fields = ['id', 'name', 'monthly_plan', 'currency']
#     template_name = 'cost/update_cost.html'
#
#     def get_success_url(self):
#         return reverse_lazy('userpage')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['id'] = self.object.id
#         return context


class CostUpdateView(FormView):

    form_class = CostForm
    template_name = 'cost/update_cost.html'

    def get(self, request, *args, **kwargs):
        cost_id = int(request.path.split('/')[-1])
        cost = Cost.objects.filter(id=cost_id).first()

        name = cost.name
        monthly_plan = cost.monthly_plan
        currency = cost.currency

        form = CostForm(initial={'name': name,
                                 'monthly_plan': monthly_plan,
                                 'currency': currency})

        return render(request, template_name=self.template_name,
                      context={'form': form})

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        monthly_plan = form.cleaned_data.get('monthly_plan')
        currency = form.cleaned_data.get('currency')
        Cost.objects.filter(id=int(self.request.path.split('/')[-1])).update(
            name=name, monthly_plan=monthly_plan, currency=currency)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('userpage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = self.object.id
        return context