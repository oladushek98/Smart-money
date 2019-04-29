import datetime

from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, F

from main.forms import ReportGenerationForm
from main.models import Transaction, Income, Account, Cost
from main.utils import PDFConverter


class ReportParameterView(LoginRequiredMixin, FormView):
    form_class = ReportGenerationForm
    template_name = 'report/report_parameters.html'

    def form_valid(self, form):
        self.period = form.cleaned_data.get('period')
        self.nodes = form.cleaned_data.get('nodes')
        self.date = self.request.POST['calendar']

        return super().form_valid(form)

    def get_success_url(self):
        temp = self.request.path.split('/')
        temp[-2] = 'generation'
        temp = '/'.join(temp)

        return temp + f'?period={self.period}&nodes={self.nodes}&date={self.date}'


class ReportGenerationView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        transactions = None

        date = datetime.datetime.strptime(request.GET['date'], '%b %d, %Y')

        if request.path.endswith('day/'):
            transactions = Transaction.objects.filter(data_from=datetime.datetime.today().date(),
                                                      user_id=request.user.id).prefetch_related('transaction_from',
                                                                                                'transaction_to').all()

        elif request.path.endswith('month/'):
            transactions = Transaction.objects.filter(data_from__month=datetime.datetime.today().month,
                                                      data_from__year=datetime.datetime.today().year,
                                                      user_id=request.user.id).prefetch_related('transaction_from',
                                                                                                'transaction_to').all()

        elif request.path.endswith('week/'):
            transactions = Transaction.objects.filter(
                                                      data_from__week=datetime.datetime.today().isocalendar()[1],
                                                      user_id=request.user.id).prefetch_related('transaction_from',
                                                                                                'transaction_to').all()

        elif request.path.endswith('year/'):
            transactions = Transaction.objects.filter(
                                                      data_from__year=datetime.datetime.today().year,
                                                      user_id=request.user.id).prefetch_related('transaction_from',
                                                                                                'transaction_to').all()

        incomes = Income.objects.filter(user_id=request.user.id, delete=False)
        accounts = Account.objects.filter(user_id=request.user.id, delete=False)
        costs = Cost.objects.filter(user_id=request.user.id, delete=False)

        context = {
            'transactions': transactions,
            'incomes': incomes,
            'accounts': accounts,
            'costs': costs
        }
        pdf = PDFConverter.render_to_pdf('report/report.html', context)

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = f'Report_{request.user.username}_{request.path.split("/")[-2]}'
            content = f'inline; filename=\'{filename}\''
            download = request.GET.get("download")

            if download:
                content = f'attachment; filename=\'{filename}\''

            response['Content-Disposition'] = content

            return response

        return HttpResponse('Not found!')
