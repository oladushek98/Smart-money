import json

from django.db.models import Q, Sum
from django.shortcuts import render

from main.forms import CostForm
from main.models import Cost, Transaction
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

    def get_history_from_chart_data(self, cost):
        source_query = list(Transaction.objects.filter(
            Q(transaction_to=cost.id) & Q(delete=False) & Q(
                user=self.request.user.id))
                            .order_by('transaction_from__id')
                            .values('transaction_from__name')
                            .annotate(Sum('amount')))
        res = [list(cost.values()) for cost in source_query]
        for item in res:
            item[0] = item[0].replace('"', '~')
        return res

    def get(self, request, *args, **kwargs):
        cost_id = int(request.path.split('/')[-1])
        cost = Cost.objects.filter(id=cost_id).first()

        name = cost.name
        monthly_plan = cost.monthly_plan
        currency = cost.currency

        form = CostForm(initial={'name': name,
                                 'monthly_plan': monthly_plan,
                                 'currency': currency})

        form.id = cost_id

        source_history = self.get_history_from_chart_data(cost)

        return render(request, template_name=self.template_name,
                      context={'form': form,
                               'data_from': json.dumps(source_history)})

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