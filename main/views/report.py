import datetime

from django.http import HttpResponse
from django.views.generic import FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin

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
        print(self.request.user.username)

        return temp + f'?period={self.period}&nodes={self.nodes}&date={self.date}'


class ReportGenerationView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        transactions = None
        temp = None

        period = request.GET['period']
        nodes = request.GET['nodes']
        date = datetime.datetime.strptime(request.GET['date'], '%b %d, %Y')

        if period == 'day':
            temp = date
            date += datetime.timedelta(days=1)
            transactions = Transaction.objects.filter(data_from=temp,
                                                      user_id=request.user.id).prefetch_related('transaction_from',
                                                                                                'transaction_to').all()

        elif period == 'month':
            temp = date - datetime.timedelta(days=30)
            transactions = Transaction.objects.filter(data_from__gte=temp,
                                                      # data_from__year=temp.year,
                                                      user_id=request.user.id).prefetch_related('transaction_from',
                                                                                                'transaction_to').all()

        elif period == 'week':
            temp = date - datetime.timedelta(days=7)
            transactions = Transaction.objects.filter(
                                                      data_from__gte=temp,
                                                      user_id=request.user.id).prefetch_related('transaction_from',
                                                                                                'transaction_to').all()

        elif period == 'year':
            temp = date - datetime.timedelta(days=365)
            transactions = Transaction.objects.filter(
                                                      data_from__gte=temp,
                                                      user_id=request.user.id).prefetch_related('transaction_from',
                                                                                                'transaction_to').all()

        elif period == 'whole':
            temp = 'beginning'
            transactions = Transaction.objects.filter(
                                                      user_id=request.user.id).prefetch_related('transaction_from',
                                                                                                'transaction_to').all()

        context = {
            'transaction': transactions,
            'period': f', your report from {temp} to {date}',
            'user': f'Dear {request.user.username.title()}',
        }

        if 'incomes' in nodes:
            incomes = Income.objects.filter(user_id=request.user.id, delete=False)
            context['incomes'] = incomes
        if 'accounts' in nodes:
            accounts = Account.objects.filter(user_id=request.user.id, delete=False)
            context['accounts'] = accounts
        if 'costs' in nodes:
            costs = Cost.objects.filter(user_id=request.user.id, delete=False)
            context['costs'] = costs

        pdf = PDFConverter.render_to_pdf('report/report.html', context)

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = f'Report_{request.user.username}_{period}_from_{temp}_to_{date}'
            content = f'inline; filename=\'{filename}\''
            download = request.GET.get("download")

            if download:
                content = f'attachment; filename=\'{filename}\''

            response['Content-Disposition'] = content

            return response

        return HttpResponse('Not found!')
