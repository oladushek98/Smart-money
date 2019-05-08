from django.shortcuts import render

from main.forms import IncomeForm
from main.models import Income
from django.urls import reverse_lazy
from django.views.generic import UpdateView, FormView, CreateView


class IncomeUpdateView(FormView):
    form_class = IncomeForm
    template_name = 'income/update_income.html'

    def get(self, request, *args, **kwargs):
        income_id = int(request.path.split('/')[-1])
        income = Income.objects.filter(id=income_id).first()

        name = income.name
        monthly_plan = income.monthly_plan
        currency = income.currency

        form = IncomeForm(initial={'name': name,
                                   'monthly_plan': monthly_plan,
                                   'currency': currency})

        form.id = income.id
        return render(request, template_name=self.template_name,
                      context={'form': form})

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        monthly_plan = form.cleaned_data.get('monthly_plan')
        currency = form.cleaned_data.get('currency')
        Income.objects.filter(id=int(self.request.path.split('/')[-1])).update(
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
